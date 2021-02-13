from functools import wraps
from typing import Callable, Union

from genki.http.url import URL

DEFAULT_API_SERVER = URL("https://api.telegram.org/")


addr = Union[URL, str]


def own_result(func: Callable):
    """Decorator to automatically set bot instance
    for method's result
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        result._bot = self
        return result
    return wrapper
