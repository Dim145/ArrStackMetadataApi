from fastapi import APIRouter

from routers.v1.tmdb.movies import movieRouter

moviesRouter = APIRouter(prefix="/movie")

moviesRouter.include_router(router=movieRouter)