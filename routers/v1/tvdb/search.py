import asyncio
from datetime import timedelta

from fastapi import APIRouter
from tmdbsimple import Search

from env import USE_TMDB_FOR_SONARR, LANGS_FALLBACK, INCLUDE_ADULT_CONTENT
from models.skyhook.tvdb.show import Show
from routers.cache import router_cache
from routers.v1.tvdb import shows
from utils import CACHE_TVDB_SEARCH_PREFIX, cache_or_exec, CACHE_TVDB_SHOW_PREFIX, CACHE_SERVER_RESPONSE_PREFIX, \
    CACHE_TMDB_SEARCH_TV_PREFIX, set_attrs_from_dict

searchRouter = APIRouter(prefix="/search/en") # always use en lang at this time

@searchRouter.get("/")
@router_cache(CACHE_SERVER_RESPONSE_PREFIX + 'tvdb_search_{term}', expire=timedelta(hours=1))
async def search(term: str):
    results = []

    if USE_TMDB_FOR_SONARR:
        s = Search()

        cache_id = CACHE_TMDB_SEARCH_TV_PREFIX + term
        res = cache_or_exec(cache_id, lambda: s.tv(query=term, language=LANGS_FALLBACK[0].pt1,
                                                           include_adult=INCLUDE_ADULT_CONTENT))

        if not hasattr(s, 'results'):
            set_attrs_from_dict(s, res)

        # tmdb  doen't return all infos. Need to fetch each show separately
        tasks = [shows.get_shows(tv.get("id")) for tv in res.results]
        responses = await asyncio.gather(*tasks)

        results.extend(responses)
    else:
        from routers.v1.tvdb import TVDB_API

        cache_id = CACHE_TVDB_SEARCH_PREFIX + str(term)

        tvdb_search_result = cache_or_exec(cache_id, lambda: TVDB_API.search(term, primary_type="series"),
                                           expire=timedelta(hours=3))

        for search_result in tvdb_search_result:
            tvdb_id = search_result.get('tvdb_id')
            serie_cache_id = CACHE_TVDB_SHOW_PREFIX + str(tvdb_id)

            try:
                serie_result = cache_or_exec(serie_cache_id,
                                             lambda: TVDB_API.get_series_extended(search_result.get('tvdb_id'),
                                                                                  meta="translations"),
                                             expire=timedelta(days=1))

                if serie_result:
                    results.append(Show.from_tvdb_obj(serie_result))
            except ValueError as e:
                # If the series is not found, we skip it
                if "not found" in str(e).lower():
                    continue
                else:
                    raise e

    return results