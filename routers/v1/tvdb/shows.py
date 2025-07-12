from datetime import timedelta

from fastapi import APIRouter

from env import USE_TMDB_FOR_SONARR, LANGS_FALLBACK
from models.skyhook.tvdb.show import Show, Episode
from routers.cache import router_cache
from utils import cache_or_exec, CACHE_TVDB_SHOW_PREFIX, CACHE_EPISODES_SUFFIX, CACHE_SERVER_RESPONSE_PREFIX, \
    CACHE_TMDB_TV_PREFIX, CACHE_TMDB_EPISODE_GROUP_PREFIX, TMDB_TVDBD_EPISODE_ORDER_NAME

showsRouter = APIRouter(prefix="/shows/en") # always use en lang at this time

@showsRouter.get("/{tvdb_id}")
@router_cache(CACHE_SERVER_RESPONSE_PREFIX + 'tvdb_shows_{tvdb_id}', expire=timedelta(hours=1))
async def get_shows(tvdb_id: int):
    if USE_TMDB_FOR_SONARR:
        import tmdbsimple as tmdb_client

        cache_id = CACHE_TMDB_TV_PREFIX + str(tvdb_id)
        tv = tmdb_client.TV(tvdb_id)
        tmdb_response = cache_or_exec(cache_id, lambda: tv.info(append_to_response="external_ids,content_ratings,credits,alternatives_titles,images,episode_groups,translations", language=""))

        # get episode groups with tvdb order
        episode_groups = tmdb_response.get('episode_groups', {}).get('results', [])
        if len(episode_groups) > 0:
            episode_group = None

            for group in episode_groups:
                if group.get('name') == TMDB_TVDBD_EPISODE_ORDER_NAME:
                    episode_group = group
                    break

            if episode_group:
                cache_id = CACHE_TMDB_EPISODE_GROUP_PREFIX + str(episode_group.get('id'))
                episode_group = cache_or_exec(cache_id, lambda: tmdb_client.TV_Episode_Groups(episode_group.get('id')).info())

                tmdb_response['tvdb_episode_group'] = episode_group

        # todo: if no episode groups or no tvdb ordering, get episodes from tmdb orders

        return Show.from_tmdb_obj(tmdb_response)
    else:
        from routers.v1.tvdb import TVDB_API

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
                                     lambda: TVDB_API.get_series_episodes(tvdb_id, season_type="default", page=count,
                                                                          lang="eng"))

            tmp = response.get('episodes', [])

            if len(tmp) == 0:
                break
            else:
                count += 1
                tvdb_episodes.extend(tmp)

        show.episodes = [Episode.from_tvdb_obj(tvdb_episode) for tvdb_episode in tvdb_episodes]

        return show