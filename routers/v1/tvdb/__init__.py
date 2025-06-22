import tvdb_v4_official
from fastapi import APIRouter

from routers.v1.tvdb.search import searchRouter
from routers.v1.tvdb.shows import showsRouter
from env import TVDB_API_KEY

TVDB_API = tvdb_v4_official.TVDB(TVDB_API_KEY)

tvdbRouter = APIRouter(prefix="/tvdb")

@tvdbRouter.get("/")
async def root():
    return {"message": "Welcome to the v1 tvdb API"}

tvdbRouter.include_router(router=showsRouter)
tvdbRouter.include_router(router=searchRouter)