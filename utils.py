
def cache_or_exec(cache_id: str, func: callable, expire: int = 3600) -> any:
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