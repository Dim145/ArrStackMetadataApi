import tvdb_v4_official
from datetime import timedelta, datetime

from fastapi import APIRouter

from env import USE_TMDB_FOR_SONARR, LANGS_FALLBACK
from models.skyhook.tvdb.show import Show, Episode
from routers.cache import router_cache
from utils import cache_or_exec, CACHE_TVDB_SHOW_PREFIX, CACHE_EPISODES_SUFFIX, CACHE_SERVER_RESPONSE_PREFIX, \
    CACHE_TMDB_TV_PREFIX, CACHE_TMDB_EPISODE_GROUP_PREFIX, TMDB_TVDB_EPISODE_ORDER_NAME, CACHE_SEASON_SUFFIX, \
    TMDB_IMAGE_BASE_URL, get_tmdb_only_ids_from_pc

showsRouter = APIRouter(prefix="/shows/en") # always use en lang at this time

@showsRouter.get("/{tvdb_id}")
@router_cache(CACHE_SERVER_RESPONSE_PREFIX + 'tvdb_shows_{tvdb_id}', expire=timedelta(hours=1))
async def get_shows(tvdb_id: int, adult: bool = False, ignore_not_found: bool = False):
    use_tmdb = USE_TMDB_FOR_SONARR or adult

    if not use_tmdb and str(tvdb_id) in get_tmdb_only_ids_from_pc():
        use_tmdb = True

    if use_tmdb:
        import tmdbsimple as tmdb_client

        parsed_id = tvdb_id

        cache_id = CACHE_TMDB_TV_PREFIX + str(parsed_id)
        tv = tmdb_client.TV(parsed_id)
        tmdb_response = cache_or_exec(cache_id, lambda: tv.info(append_to_response="external_ids,content_ratings,credits,alternatives_titles,images,episode_groups,translations", language=""))

        # get episode groups with tvdb order
        episode_groups = tmdb_response.get('episode_groups', {}).get('results', [])
        if len(episode_groups) > 0:
            episode_group = None

            for group in episode_groups:
                if group.get('name') == TMDB_TVDB_EPISODE_ORDER_NAME:
                    episode_group = group
                    break

            if episode_group:
                cache_id = CACHE_TMDB_EPISODE_GROUP_PREFIX + str(episode_group.get('id'))
                episode_group = cache_or_exec(cache_id, lambda: tmdb_client.TV_Episode_Groups(episode_group.get('id')).info())

                tmdb_response['tvdb_episode_group'] = episode_group

        show = Show.from_tmdb_obj(tmdb_response)

        if len(show.episodes) == 0:
            episodes = []

            for season in tmdb_response.get('seasons', []):
                season_number = season.get('season_number')
                cache_id = CACHE_TMDB_TV_PREFIX + str(parsed_id) + CACHE_SEASON_SUFFIX + f"_{season_number}"
                s = tmdb_client.TV_Seasons(parsed_id, season_number)
                season_response = cache_or_exec(cache_id, lambda: s.info(append_to_response="images,translations", language=""))

                for ep in season_response.get('episodes', []):
                    episode = Episode(
                        ep.get('show_id'),
                        ep.get('id'),
                        season_number,
                        ep.get('episode_number'),
                        len(episodes) + 1,  # absolute episode number
                        None,
                        None,
                        ep.get('name'),
                        ep.get('air_date'),
                        datetime.strptime(ep.get('air_date'), '%Y-%m-%d').strftime(
                            '%Y-%m-%dT%H:%M:%SZ') if ep.get('air_date') else None,
                        ep.get('runtime'),
                        ep.get('overview'),
                        TMDB_IMAGE_BASE_URL + ep.get('still_path') if ep.get('still_path') else None,
                        "season" if ep.get('episode_type') == "finale" else None,
                    )
                    episode.season_number = season_number
                    episodes.append(episode)

            show.episodes = episodes

        # set tvdb_id for the show with not parsed tvdb_id
        show.tvdbId = tvdb_id

        return show
    else:
        from routers.v1.tvdb import TVDB_API

        try:
            cache_id = CACHE_TVDB_SHOW_PREFIX + str(tvdb_id)
            tv = cache_or_exec(cache_id, lambda: TVDB_API.get_series_extended(tvdb_id, meta="translations"),
                               expire=timedelta(days=1))

            show = Show.from_tvdb_obj(tv)

            tvdb_episodes = []
            count = 0

            while True:
                cache_id = CACHE_TVDB_SHOW_PREFIX + str(tvdb_id) + CACHE_EPISODES_SUFFIX + f"_{count}"
                # set static eng lang for now because need of loop for each episode for lang fallback.
                response = cache_or_exec(cache_id,
                                         lambda: TVDB_API.get_series_episodes(tvdb_id, season_type="default",
                                                                              page=count,
                                                                              lang="eng"))

                tmp = response.get('episodes', [])

                if len(tmp) == 0:
                    break
                else:
                    count += 1
                    tvdb_episodes.extend(tmp)

            show.episodes = [Episode.from_tvdb_obj(tvdb_episode) for tvdb_episode in tvdb_episodes]

            return show
        except ValueError as e:
            if ignore_not_found and e.args and "not found" in str(e).lower():
                print(f"TVDB show {tvdb_id} not found, ignoring.")
                return None
            else:
                print(f"Error fetching TVDB show {tvdb_id}: {e}")
                raise e