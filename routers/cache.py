import json
import pickle
import re
from datetime import timedelta
from functools import wraps
from inspect import iscoroutinefunction

from env import REDIS_CACHE
from utils import CACHE_SERVER_RESPONSE_PREFIX


def router_cache(cache_key: str = "", expire: timedelta = timedelta(hours=6)):
    def wrapper(func):
        @wraps(func)
        async def wrapped(*args, **kwargs):
            key = cache_key

            if key == "":
                key = CACHE_SERVER_RESPONSE_PREFIX + func.__name__

            key = compile_template(key, *args, **kwargs)
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

def compile_template(template: str, *args, **kwargs):
    """
    Compiles a given template with the given args and kwargs.

    For the following template: "This is a test of {something}"

    Any of these will work:
        - compile_template('This is a test of {something}, 'this_is_the_something_text')
        - compile_template('This is a test of {something}, something='this_is_the_something_text')

    :param template: string template
    :param args: arguments tuple
    :param kwargs: arguments dict
    :return: template with values format
    """
    data = kwargs.copy()
    keys = re.findall('([^{]+(?=}))', template)

    i = 0
    for k in keys:
        if k not in data.keys():
            data.update({k: args[i]})
            i += 1

    return template.format(**data)