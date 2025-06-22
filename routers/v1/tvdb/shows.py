from datetime import timedelta
from traceback import print_list

from fastapi import APIRouter
from models.skyhook.tvdb.show import Show, Episode
from routers.cache import router_cache
from utils import cache_or_exec, CACHE_TVDB_SHOW_PREFIX, CACHE_EPISODES_SUFFIX, CACHE_SERVER_RESPONSE_PREFIX

showsRouter = APIRouter(prefix="/shows/en") # always use en lang at this time

@showsRouter.get("/{tvdb_id}")
@router_cache(expire=timedelta(hours=1))
async def get_shows(tvdb_id: int):
    from routers.v1.tvdb import TVDB_API

    cache_id = CACHE_TVDB_SHOW_PREFIX + str(tvdb_id)
    tv = cache_or_exec(cache_id, lambda: TVDB_API.get_series_extended(tvdb_id, meta="translations"))

    show = Show.from_tvdb_obj(tv)

    # Set the language for the show
    cache_id = CACHE_TVDB_SHOW_PREFIX + str(tvdb_id) + CACHE_EPISODES_SUFFIX
    tvdb_episodes = cache_or_exec(cache_id, lambda: TVDB_API.get_series_episodes(tvdb_id, season_type="default", page=0))

    show.episodes = [Episode.from_tvdb_obj(tvdb_episode) for tvdb_episode in tvdb_episodes.get('episodes', [])]

    return show