from datetime import timedelta

from fastapi import APIRouter

from models.skyhook.tvdb.show import Show
from routers.cache import router_cache
from utils import CACHE_TVDB_SEARCH_PREFIX, cache_or_exec, CACHE_TVDB_SHOW_PREFIX, CACHE_SERVER_RESPONSE_PREFIX

searchRouter = APIRouter(prefix="/search/en") # always use en lang at this time

@searchRouter.get("/")
@router_cache(CACHE_SERVER_RESPONSE_PREFIX + 'tvdb_search_{term}', expire=timedelta(hours=1))
async def search(term: str):
    from routers.v1.tvdb import TVDB_API

    cache_id = CACHE_TVDB_SEARCH_PREFIX + str(term)

    tvdb_search_result = cache_or_exec(cache_id, lambda: TVDB_API.search(term, primary_type="series"), expire=timedelta(hours=3))

    results = []

    for search_result in tvdb_search_result:
        tvdb_id = search_result.get('tvdb_id')
        serie_cache_id = CACHE_TVDB_SHOW_PREFIX + str(tvdb_id)

        try:
            serie_result = cache_or_exec(serie_cache_id,
                                         lambda: TVDB_API.get_series_extended(search_result.get('tvdb_id'),
                                                                              meta="translations"), expire=timedelta(days=1))

            if serie_result:
                results.append(Show.from_tvdb_obj(serie_result))
        except ValueError as e:
            # If the series is not found, we skip it
            if "not found" in str(e).lower():
                continue
            else:
                raise e

    return results