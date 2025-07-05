from datetime import timedelta

CACHE_TVDB_SHOW_PREFIX = 'tvdb_show_'
CACHE_EPISODES_SUFFIX = '_episodes'
CACHE_TVDB_SEARCH_PREFIX = 'tvdb_search_'

CACHE_TMDB_MOVIE_PREFIX = 'tmdb_movie_'
CACHE_TMDB_COLLECTION_PREFIX = 'tmdb_collection_'
CACHE_TMDB_RELEASE_DATES_SUFFIX = '_release_dates'
CACHE_TMDB_CHANGED_PREFIX = 'tmdb_changed_'
CACHE_TMDB_POPULAR_PREFIX = 'tmdb_popular_'
CACHE_TMDB_SEARCH_PREFIX = 'tmdb_search_'

CACHE_IMAGES_SUFFIX = '_images'
CACHE_KEYWORDS_SUFFIX = '_keywords'
CACHE_TRANSLATIONS_SUFFIX = '_translations'
CACHE_RECOMMENDATIONS_SUFFIX = '_recommendations'
CACHE_CREDITS_SUFFIX = '_credits'
CACHE_ALTERNATIVE_TITLES_SUFFIX = '_alternative_titles'
CACHE_VIDEOS_SUFFIX = '_videos'

CACHE_SERVER_RESPONSE_PREFIX = 'cache_server_response_'

TMDB_IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/original'

def cache_or_exec(cache_id: str, func: callable, expire: timedelta = timedelta(hours=6)) -> any:
    """
    Cache the result of a function call based on an ID.

    Parameters:
    - id: Unique identifier for the cache key.
    - func: Function to execute if the cache is empty.
    - expire: Cache expiration time in seconds (default is 3600 seconds).

    Returns:
    The cached result or the result of the function call.
    """
    from env import REDIS_CACHE

    cached_result = REDIS_CACHE.get(cache_id)

    if cached_result:
        # parse json if result is a json string
        if cached_result.startswith('{') or cached_result.startswith('['):
            import json
            try:
                cached_result = json.loads(cached_result)
            except json.JSONDecodeError:
                pass

        return cached_result

    result = func()
    cached_result = result

    # transform result to string to save in redis
    if isinstance(result, (list, dict)):
        import json
        cached_result = json.dumps(result)
    elif not isinstance(result, str):
        cached_result = str(result)

    REDIS_CACHE.set(cache_id, cached_result, ex=expire)

    return result

def set_attrs_from_dict(obj: object, data: dict) -> None:
    if isinstance(data, dict):
        for key in data.keys():
            if not hasattr(obj, key) or not callable(getattr(obj, key)):
                setattr(obj, key, data[key])