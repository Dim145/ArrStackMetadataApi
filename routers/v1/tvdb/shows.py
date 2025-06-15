from fastapi import APIRouter

showsRouter = APIRouter(prefix="/shows/en") # always use en lang at this time

@showsRouter.get("/{tvdb_id}")
async def get_shows(tvdb_id: int):
    from routers.v1.tvdb import TVDB_API

    tv = TVDB_API.get_series_extended(tvdb_id)

    return {
        "message": f"tvdb_id: {tvdb_id}",
        "data": tv
    }