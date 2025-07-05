import asyncio
from datetime import timedelta, datetime
from typing import List

from fastapi import APIRouter

import tmdbsimple as tmdb_client
from tmdbsimple import Changes, Collections

from env import LANGS_FALLBACK
from models.skyhook.tmdb.collection import Collection
from models.skyhook.tmdb.movie import Movie
from routers.cache import router_cache
from utils import CACHE_TMDB_MOVIE_PREFIX, cache_or_exec, set_attrs_from_dict, CACHE_TMDB_RELEASE_DATES_SUFFIX, \
    CACHE_IMAGES_SUFFIX, CACHE_KEYWORDS_SUFFIX, CACHE_TRANSLATIONS_SUFFIX, CACHE_RECOMMENDATIONS_SUFFIX, \
    CACHE_CREDITS_SUFFIX, CACHE_ALTERNATIVE_TITLES_SUFFIX, CACHE_VIDEOS_SUFFIX, CACHE_SERVER_RESPONSE_PREFIX, \
    CACHE_TMDB_CHANGED_PREFIX, CACHE_TMDB_COLLECTION_PREFIX

movieRouter = APIRouter()

@movieRouter.get("/")
async def root():
    return {"message": "Welcome to the v1 movie API"}

@movieRouter.get("/changed")
@router_cache(CACHE_SERVER_RESPONSE_PREFIX + 'tmdb_changed_{since}', expire=timedelta(hours=1))
def get_changed(since: datetime = None):
    changes = Changes()

    response = []

    while True:

        page = 1
        while True:

            cache_id = CACHE_TMDB_CHANGED_PREFIX + "movie_" + since.strftime('%Y-%m-%d') + f'_{page}'
            since_str = since.strftime('%Y-%m-%d') if since else None
            tmdb_response = cache_or_exec(cache_id, lambda: changes.movie(start_date=since_str, page=page), expire=timedelta(days=7))
            results =  tmdb_response.get('results', None)

            if not results or len(results) == 0:
                break

            response.extend(map(lambda r: r.get("id"), results))
            page += 1

        if not since or datetime.now() - since <= timedelta(hours=1):
            break

        since = since + timedelta(days=14)


    return response

@movieRouter.get("/collection/{tmdb_id}")
@router_cache(CACHE_SERVER_RESPONSE_PREFIX + 'tmdb_collection_{tmdb_id}', expire=timedelta(hours=1))
async def get_collection(tmdb_id: str):

    collection = Collections(tmdb_id)

    cache_id = CACHE_TMDB_COLLECTION_PREFIX + str(tmdb_id)
    tmdb_response = cache_or_exec(cache_id, lambda: collection.info(language=LANGS_FALLBACK[0].pt1))

    if not hasattr(collection, 'name'):
        set_attrs_from_dict(collection, tmdb_response)

    cache_id = CACHE_TMDB_COLLECTION_PREFIX + str(tmdb_id) + CACHE_IMAGES_SUFFIX
    images_response = cache_or_exec(cache_id, lambda: collection.images(include_image_language=map(lambda x: x.pt1, LANGS_FALLBACK)))

    if not hasattr(collection, 'backdrops'):
        set_attrs_from_dict(collection, images_response)

    cache_id = CACHE_TMDB_COLLECTION_PREFIX + str(tmdb_id) + CACHE_TRANSLATIONS_SUFFIX
    translations_response = cache_or_exec(cache_id, lambda: collection.translations())

    collection.translations = translations_response.get('translations', [])

    response = Collection.from_tmdb_obj(collection)

    tasks = [get_movie(part.get("id")) for part in collection.parts]
    movies = await asyncio.gather(*tasks)
    response.Parts = movies


    return response

@movieRouter.get("/{tmdb_id}")
@router_cache(CACHE_SERVER_RESPONSE_PREFIX + 'tmdb_movies_{tmdb_id}', expire=timedelta(hours=1))
async def get_movie(tmdb_id: int):
    # use append_to_response=videos,release_dates,images,keywords,alternative_titles,translations,recommendations,credits,videos ?

    cache_id = CACHE_TMDB_MOVIE_PREFIX + str(tmdb_id)
    movie = tmdb_client.Movies(tmdb_id)
    tmdb_response = cache_or_exec(cache_id, lambda: movie.info(language=LANGS_FALLBACK[0].pt1))

    # re-set movie object attributes with tmdb_response data for cached tmdb_response
    if not hasattr(movie, 'title'):
        set_attrs_from_dict(movie, tmdb_response)

    cache_id = CACHE_TMDB_MOVIE_PREFIX + str(tmdb_id) + CACHE_TMDB_RELEASE_DATES_SUFFIX
    rd_response = cache_or_exec(cache_id, lambda: movie.release_dates())

    movie.release_dates_by_country = rd_response.get('results', [])

    cache_id = CACHE_TMDB_MOVIE_PREFIX + str(tmdb_id) + CACHE_IMAGES_SUFFIX
    images_response = cache_or_exec(cache_id, lambda: movie.images(include_image_language=map(lambda x: x.pt1, LANGS_FALLBACK)))

    if not hasattr(movie, 'backdrops'):
        set_attrs_from_dict(movie, images_response)

    cache_id = CACHE_TMDB_MOVIE_PREFIX + str(tmdb_id) + CACHE_KEYWORDS_SUFFIX
    keywords_response = cache_or_exec(cache_id, lambda: movie.keywords())

    movie.keywords = keywords_response.get('keywords', [])

    cache_id = CACHE_TMDB_MOVIE_PREFIX + str(tmdb_id) + CACHE_ALTERNATIVE_TITLES_SUFFIX
    alternative_titles_response = cache_or_exec(cache_id, lambda: movie.alternative_titles())

    movie.alternative_titles = alternative_titles_response.get('titles', [])

    cache_id = CACHE_TMDB_MOVIE_PREFIX + str(tmdb_id) + CACHE_TRANSLATIONS_SUFFIX
    translations_response = cache_or_exec(cache_id, lambda: movie.translations())

    movie.translations = translations_response.get('translations', [])

    cache_id = CACHE_TMDB_MOVIE_PREFIX + str(tmdb_id) + CACHE_RECOMMENDATIONS_SUFFIX
    recommendations_response = cache_or_exec(cache_id, lambda: movie.recommendations())

    movie.recommendations = recommendations_response.get('results', [])


    cache_id = CACHE_TMDB_MOVIE_PREFIX + str(tmdb_id) + CACHE_CREDITS_SUFFIX
    credits_response = cache_or_exec(cache_id, lambda: movie.credits())

    if not hasattr(movie, 'cast'):
        set_attrs_from_dict(movie, credits_response)

    cache_id = CACHE_TMDB_MOVIE_PREFIX + str(tmdb_id) + CACHE_VIDEOS_SUFFIX
    videos_response = cache_or_exec(cache_id, lambda: movie.videos())

    movie.videos = videos_response.get('results', [])

    response = Movie.from_tmdb_obj(movie)

    return response

@movieRouter.post("/bulk")
@router_cache(CACHE_SERVER_RESPONSE_PREFIX + 'tmdb_movies_bulk_{tmdb_ids}', expire=timedelta(hours=1))
async def get_movie_bulk(tmdb_ids: List[int]):

    tasks = [get_movie(tmdb_id) for tmdb_id in tmdb_ids]
    movie_responses = await asyncio.gather(*tasks)

    return movie_responses

@movieRouter.get("/imdb/{imdb_id}")
@router_cache(CACHE_SERVER_RESPONSE_PREFIX + 'tmdb_imdb_{imdb_id}', expire=timedelta(hours=1))
async def get_movie_by_imdb(imdb_id: str):

    find = tmdb_client.Find(imdb_id)

    cache_id = CACHE_TMDB_MOVIE_PREFIX + "imdb_" + imdb_id
    movie = cache_or_exec(cache_id, lambda: find.info(external_source='imdb_id'), expire=timedelta(days=14))

    if not hasattr(find, 'movie_results'):
        set_attrs_from_dict(find, movie)

    tasks = [get_movie(movie_result.get("id")) for movie_result in find.movie_results]
    movie_responses = await asyncio.gather(*tasks)

    return movie_responses