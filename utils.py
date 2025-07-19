import os
import pathlib
from datetime import timedelta
from time import sleep

from env import ROOT_DATA_PATH

CACHE_TVDB_SHOW_PREFIX = 'tvdb_show_'
CACHE_EPISODES_SUFFIX = '_episodes'
CACHE_TVDB_SEARCH_PREFIX = 'tvdb_search_'

CACHE_TMDB_MOVIE_PREFIX = 'tmdb_movie_'
CACHE_TMDB_TV_PREFIX = 'tmdb_tv_'
CACHE_TMDB_COLLECTION_PREFIX = 'tmdb_collection_'
CACHE_TMDB_RELEASE_DATES_SUFFIX = '_release_dates'
CACHE_TMDB_CHANGED_PREFIX = 'tmdb_changed_'
CACHE_TMDB_POPULAR_PREFIX = 'tmdb_popular_'
CACHE_TMDB_SEARCH_PREFIX = 'tmdb_search_'
CACHE_TMDB_SEARCH_TV_PREFIX = 'tmdb_search_tv_'
CACHE_TMDB_EPISODE_GROUP_PREFIX = 'tmdb_episode_group_'

CACHE_MUSICBRAINZ_ALBUM_PREFIX = 'musicbrainz_album_'

CACHE_IMAGES_SUFFIX = '_images'
CACHE_KEYWORDS_SUFFIX = '_keywords'
CACHE_TRANSLATIONS_SUFFIX = '_translations'
CACHE_RECOMMENDATIONS_SUFFIX = '_recommendations'
CACHE_EXTERNAL_IDS_SUFFIX = '_external_ids'
CACHE_CREDITS_SUFFIX = '_credits'
CACHE_ALTERNATIVE_TITLES_SUFFIX = '_alternative_titles'
CACHE_VIDEOS_SUFFIX = '_videos'
CACHE_SEASON_SUFFIX = '_season'

CACHE_SERVER_RESPONSE_PREFIX = 'cache_server_response_'

PERSISTENT_CACHE_PREFIX = 'persistent_cache_'

TMDB_IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/original'
TMDB_TVDB_EPISODE_ORDER_NAME = 'TVDB Order'

TMDB_ID_PREFIX = '989'

def exec_and_wait(func: callable, seconds: int = 1) -> any:
    """
    Execute a function and wait for a specified number of seconds.

    Parameters:
    - func: Function to execute.
    - seconds: Number of seconds to wait after execution (default is 1 second).

    Returns:
    The result of the function call.
    """

    result = func()
    sleep(seconds)
    return result

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

def get_tmdb_only_ids_from_pc():
    """
    Fetches TMDB IDs from the persistent cache.
    Used when TMDB is not the main data source but adult content is included.

    Returns:
    A list of TMDB IDs.
    """
    from env import REDIS_CACHE

    ids = str(REDIS_CACHE.get(PERSISTENT_CACHE_PREFIX + 'tmdb_ids') or "").strip()

    return ids.split(',') if ids and len(ids) > 0 else []

def add_tmdb_only_ids_to_pc(tmdb_ids) -> None:
    """
    Adds TMDB IDs to the persistent cache.

    Parameters:
    - tmdb_ids: List of TMDB IDs to add.
    """
    from env import REDIS_CACHE

    current_ids = get_tmdb_only_ids_from_pc()

    # if tmdb_ids is iterable, extend current_ids
    if hasattr(tmdb_ids, '__iter__'):
        current_ids.extend(str(id) for id in tmdb_ids)
    else:
        current_ids.append(str(tmdb_ids))

    current_ids = list(set(current_ids))  # remove duplicates
    REDIS_CACHE.set(PERSISTENT_CACHE_PREFIX + 'tmdb_ids', ','.join(current_ids))

async def save_tmdb_ids_to_file():
    """
    Saves TMDB IDs from the persistent cache to a file.
    """

    ids = get_tmdb_only_ids_from_pc()

    # data directory doesn't exist, create it
    os.makedirs(pathlib.Path(ROOT_DATA_PATH), exist_ok=True)

    path = pathlib.Path(ROOT_DATA_PATH, 'tmdb_ids.txt')
    if not path.exists():
        path.touch()

    with open(path, 'w') as f:
        f.write('\n'.join(ids))

def load_tmdb_ids_from_file():
    """
    Loads TMDB IDs from a file into the persistent cache.
    """

    path = pathlib.Path(ROOT_DATA_PATH, 'tmdb_ids.txt')

    # data directory doesn't exist, create it
    path.parent.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        path.touch()

    with path.open('r') as f:
        ids = f.read().strip().split('\n')

    add_tmdb_only_ids_to_pc(ids)

# load TMDB IDs from a file at startup
load_tmdb_ids_from_file()