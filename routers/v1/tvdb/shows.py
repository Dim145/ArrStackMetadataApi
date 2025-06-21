from fastapi import APIRouter

from env import TVDB_RESULT_LANG
from models.skyhook.tvdb.show import Show, Episode

showsRouter = APIRouter(prefix="/shows/en") # always use en lang at this time

@showsRouter.get("/{tvdb_id}")
async def get_shows(tvdb_id: int):
    from routers.v1.tvdb import TVDB_API

    tv = TVDB_API.get_series_extended(tvdb_id, meta="translations")

    show = Show.from_tvdb_obj(tv)

    tvdb_episodes = TVDB_API.get_series_episodes(tvdb_id, season_type="default", page=0)

    show.episodes = [Episode.from_tvdb_obj(tvdb_episode) for tvdb_episode in tvdb_episodes]

    return {
        "message": f"tvdb_id: {tvdb_id}",
        "data": show
    }