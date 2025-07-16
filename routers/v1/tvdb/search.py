import asyncio
from datetime import timedelta
from fastapi import APIRouter
from tmdbsimple import Search, TV

from env import USE_TMDB_FOR_SONARR, LANGS_FALLBACK, INCLUDE_ADULT_CONTENT
from models.skyhook.tvdb.show import Show
from routers.cache import router_cache
from routers.v1.tvdb import shows
from utils import CACHE_TVDB_SEARCH_PREFIX, cache_or_exec, CACHE_TVDB_SHOW_PREFIX, CACHE_SERVER_RESPONSE_PREFIX, \
    CACHE_TMDB_SEARCH_TV_PREFIX, set_attrs_from_dict, TMDB_ID_PREFIX, CACHE_TMDB_TV_PREFIX, CACHE_EXTERNAL_IDS_SUFFIX

searchRouter = APIRouter(prefix="/search/en") # always use en lang at this time

@searchRouter.get("/")
@router_cache(CACHE_SERVER_RESPONSE_PREFIX + 'tvdb_search_{term}', expire=timedelta(hours=1))
async def search(term: str):
    from routers.v1.tvdb import TVDB_API

    results = []

    if USE_TMDB_FOR_SONARR or INCLUDE_ADULT_CONTENT:
        s = Search()

        cache_id = CACHE_TMDB_SEARCH_TV_PREFIX + term
        res = cache_or_exec(cache_id, lambda: s.tv(query=term, language=LANGS_FALLBACK[0].pt1,
                                                           include_adult=INCLUDE_ADULT_CONTENT))

        if not hasattr(s, 'results'):
            set_attrs_from_dict(s, res)

        tasks = []
        external_ids_tasks = []
        for tv in res.get('results', []):
            tv_id = tv.get('id')

            if USE_TMDB_FOR_SONARR or tv.get("adult", False):
                tv_id = int(TMDB_ID_PREFIX + str(tv.get('id')))

                tasks.append(
                    shows.get_shows(tv_id, tv.get("adult", False))
                )
            else:
                external_ids_tasks.append(
                    get_tmdb_external_ids(tv_id)
                )

        external_ids = await asyncio.gather(*external_ids_tasks) if len(external_ids_tasks) > 0 else []

        for external_id in external_ids:
            tvdb_id = external_id.get('tvdb_id')

            if tvdb_id and len(str(tvdb_id)) > 0:
                tasks.append(
                    shows.get_shows(tvdb_id, False, True)
                )
            else:
                # If no TVDB ID, we assume it's a TMDB ID
                tv_id = int(TMDB_ID_PREFIX + str(external_id.get('id')))

                tasks.append(
                    shows.get_shows(tv_id)
                )

        # tmdb  doesn't return all infos. Need to fetch each show separately
        responses = await asyncio.gather(*tasks)

        # remove None results
        responses = [res for res in responses if res is not None]

        results.extend(responses)
    else:
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

async def get_tmdb_external_ids(tmdb_id: int):
    """
    Fetches external IDs for a given TMDB ID.

    Parameters:
    - tmdb_id: The TMDB ID to fetch external IDs for.

    Returns:
    A dictionary containing the external IDs.
    """
    tv = TV(tmdb_id)

    cache_id = CACHE_TMDB_TV_PREFIX + str(tmdb_id) + CACHE_EXTERNAL_IDS_SUFFIX
    return cache_or_exec(cache_id, lambda: tv.external_ids(), expire=timedelta(days=1))