import functools
from collections import OrderedDict
from collections.abc import Callable
from typing import Any, TypeVar, cast
from typing_extensions import ParamSpec

Function = TypeVar('Function', bound=Callable[..., Any])
P = ParamSpec('P')
T = TypeVar('T')


def cache(max_size: int) -> Callable[[Function], Function]:
    """
    Returns decorator, which stores result of function
    for `max_size` most recent function arguments.
    :param max_size: max amount of unique arguments to store values for
    :return: decorator, which wraps any function passed
    """

    def wraps(func: Function) -> Callable[P, T]:
        cache_dict: OrderedDict[P.args, T] = OrderedDict()

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            if args in cache_dict:
                return cache_dict[args]
            ans = func(*args, **kwargs)
            if len(cache_dict) == max_size:
                cache_dict.popitem(last=False)
            cache_dict[args] = ans
            return ans

        return cast(Function, wrapper)

    return cast(Callable[[Function], Function], wraps)
