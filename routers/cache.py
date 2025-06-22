import json
import pickle
from datetime import timedelta
from functools import wraps
from inspect import iscoroutinefunction

from env import REDIS_CACHE

def router_cache(expire: timedelta = timedelta(hours=6)):
    def wrapper(func):
        @wraps(func)
        async def wrapped(*args, **kwargs):
            key_parts = [func.__name__] + list(args)
            key = "-".join(str(k) for k in key_parts)
            result = None

            reset_cache = kwargs.get('reset_cache', False)
            if reset_cache:
                await REDIS_CACHE.delete(key)
            else:
                result = REDIS_CACHE.get(key)

            if result is None:
                is_coroutine = iscoroutinefunction(func)
                if is_coroutine:
                    value = await func(*args, **kwargs)
                else:
                    value = func(*args, **kwargs)

                value_bytes = pickle.dumps(value)
                value_str = str(value_bytes, 'latin1')

                REDIS_CACHE.set(key, value_str, ex=expire)
            else:
                value_json = bytes(result, 'latin1')
                value = pickle.loads(value_json)

            return value
        return wrapped
    return wrapper
