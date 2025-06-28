import json
from datetime import timedelta

from fastapi import APIRouter

import tmdbsimple as tmdb_client

from env import LANGS_FALLBACK
from models.skyhook.tmdb.movie import Movie
from routers.cache import router_cache
from utils import CACHE_TMDB_MOVIE_PREFIX, cache_or_exec, set_attrs_from_dict, CACHE_TMDB_RELEASE_DATES_SUFFIX, \
    CACHE_IMAGES_SUFFIX, CACHE_KEYWORDS_SUFFIX, CACHE_TRANSLATIONS_SUFFIX, CACHE_RECOMMENDATIONS_SUFFIX, \
    CACHE_CREDITS_SUFFIX, CACHE_ALTERNATIVE_TITLES_SUFFIX, CACHE_VIDEOS_SUFFIX, CACHE_SERVER_RESPONSE_PREFIX

movieRouter = APIRouter()

@movieRouter.get("/")
async def root():
    return {"message": "Welcome to the v1 movie API"}

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