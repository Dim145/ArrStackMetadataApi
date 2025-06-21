from traceback import print_list

from fastapi import APIRouter

from env import TVDB_RESULT_LANG, REDIS_CACHE
from models.skyhook.tvdb.show import Show, Episode
from utils import cache_or_exec

showsRouter = APIRouter(prefix="/shows/en") # always use en lang at this time

@showsRouter.get("/{tvdb_id}")
async def get_shows(tvdb_id: int):
    from routers.v1.tvdb import TVDB_API

    cache_id = 'tvdb_show_' + str(tvdb_id)
    tv = cache_or_exec(cache_id, lambda: TVDB_API.get_series_extended(tvdb_id, meta="translations"))

    show = Show.from_tvdb_obj(tv)

    # Set the language for the show
    cache_id = 'tvdb_show_' + str(tvdb_id) + '_episodes'
    tvdb_episodes = cache_or_exec(cache_id, lambda: TVDB_API.get_series_episodes(tvdb_id, season_type="default", page=0))

    # debug
    print(f"Retrieved {len(tvdb_episodes)} episodes for show with tvdb_id: {tvdb_id}")
    # print episodes
    print(tvdb_episodes)

    show.episodes = [Episode.from_tvdb_obj(tvdb_episode) for tvdb_episode in tvdb_episodes.get('episodes', [])]

    return {
        "message": f"tvdb_id: {tvdb_id}",
        "data": show
    }