import asyncio

from fastapi import APIRouter
from tmdbsimple import Search

from env import LANGS_FALLBACK, INCLUDE_ADULT_CONTENT
from routers.v1.tmdb import movies
from utils import CACHE_TMDB_SEARCH_PREFIX, cache_or_exec, set_attrs_from_dict

searchRouter = APIRouter()

@searchRouter.get("")
async def root(q: str, year: str = None):

    search = Search()

    cache_id = CACHE_TMDB_SEARCH_PREFIX + q + (f"_{year}" if year else "")
    res = cache_or_exec(cache_id, lambda: search.movie(query=q, year=year, language=LANGS_FALLBACK[0].pt1, include_adult=INCLUDE_ADULT_CONTENT))

    if not hasattr(search, 'results'):
        set_attrs_from_dict(search, res)

    tasks = [movies.get_movie(movie.get("id")) for movie in search.results]
    responses = await asyncio.gather(*tasks)

    return responses
