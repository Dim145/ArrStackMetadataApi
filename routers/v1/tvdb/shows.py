from datetime import timedelta

from fastapi import APIRouter
from models.skyhook.tvdb.show import Show, Episode
from routers.cache import router_cache
from utils import cache_or_exec, CACHE_TVDB_SHOW_PREFIX, CACHE_EPISODES_SUFFIX, CACHE_SERVER_RESPONSE_PREFIX

showsRouter = APIRouter(prefix="/shows/en") # always use en lang at this time

@showsRouter.get("/{tvdb_id}")
@router_cache(CACHE_SERVER_RESPONSE_PREFIX + 'tvdb_shows_{tvdb_id}', expire=timedelta(hours=1))
async def get_shows(tvdb_id: int):
    from routers.v1.tvdb import TVDB_API

    cache_id = CACHE_TVDB_SHOW_PREFIX + str(tvdb_id)
    tv = cache_or_exec(cache_id, lambda: TVDB_API.get_series_extended(tvdb_id, meta="translations"), expire=timedelta(days=1))

    show = Show.from_tvdb_obj(tv)

    tvdb_episodes = []
    count = 0

    while True:
        cache_id = CACHE_TVDB_SHOW_PREFIX + str(tvdb_id) + CACHE_EPISODES_SUFFIX + f"_{count}"
        # set static eng lang for now because need of loop for each episode for lang fallback.
        response = cache_or_exec(cache_id, lambda: TVDB_API.get_series_episodes(tvdb_id, season_type="default", page=count, lang="eng"))

        tmp = response.get('episodes', [])

        if len(tmp) == 0:
            break
        else:
            count += 1
            tvdb_episodes.extend(tmp)


    show.episodes = [Episode.from_tvdb_obj(tvdb_episode) for tvdb_episode in tvdb_episodes]

    return show