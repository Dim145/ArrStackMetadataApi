from fastapi import APIRouter

from routers.v1.tmdb.lists import listsRouter
from routers.v1.tmdb.movies import movieRouter

moviesRouter = APIRouter()

moviesRouter.include_router(router=movieRouter, prefix="/movie")
moviesRouter.include_router(router=listsRouter, prefix="/list/tmdb")