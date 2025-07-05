import asyncio
from datetime import timedelta

from fastapi import APIRouter
from tmdbsimple import Movies, Discover

from env import LANGS_FALLBACK, INCLUDE_ADULT_CONTENT
from routers.cache import router_cache
from routers.v1.tmdb import movies
from utils import CACHE_TMDB_POPULAR_PREFIX, cache_or_exec, set_attrs_from_dict, CACHE_SERVER_RESPONSE_PREFIX

listsRouter = APIRouter()

@listsRouter.get("/")
async def root():
    return {"message": "Welcome to the v1 movies lists API"}

@listsRouter.get("/popular")
@router_cache(CACHE_SERVER_RESPONSE_PREFIX + 'tmdb_popular', expire=timedelta(days=1))
async def get_popular_lists():

    discover = Discover()

    cache_id = CACHE_TMDB_POPULAR_PREFIX
    res = cache_or_exec(cache_id, lambda: discover.movie(sort_by='popularity.desc', language=LANGS_FALLBACK[0].pt1, include_adult=INCLUDE_ADULT_CONTENT, page=1))

    if not hasattr(res, 'results'):
        set_attrs_from_dict(discover, res)

    tasks = [movies.get_movie(movie.get("id")) for movie in discover.results]
    results = await asyncio.gather(*tasks)

    return results

