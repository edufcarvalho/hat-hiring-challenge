import time
from functools import wraps
from typing import Any, Callable, Optional, Type

from cachetools import TLRUCache
from cachetools import cached as base_cache

from src.utils.api.schemas import Params

_cache_store: dict[str, TLRUCache] = dict()


def _get_cache(func_name: str, expire: int) -> TLRUCache:
    global _cache_store

    cache = _cache_store.setdefault(
        func_name,
        TLRUCache(
            maxsize=100,
            ttu=lambda k, v, t: t + float(expire),
            timer=lambda: time.time(),
        ),
    )
    return cache


def _key_generator(*args, **kwargs) -> tuple:
    params = kwargs.get("params")

    if isinstance(params, Params):
        return (
            params.page,
            params.page_size,
            params.orgao,
            params.ano,
            params.mes,
            params.categoria,
            params.valor_min,
            params.valor_max,
        )

    return args


def cache(
    expire: Optional[int] = 60,
    coder: Optional[Type] = None,
    key: Optional[Callable] = _key_generator,
    namespace: str = "",
    injected_dependency_namespace: str = "__fastapi_cache",
    cache_header: str = "X-Cache",
) -> Callable:
    """
    Cache decorator that wraps cachetools @cached with info=True.
    Uses TLRUCache for time-to-use expiration.
    Uses identity key (one entry per function).
    Adds cache status header (HIT/MISS) to responses.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        tlru_cache = _get_cache(func.__name__, expire)

        wrapped = base_cache(cache=tlru_cache, key=key, info=True)(func)

        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            response = kwargs.get("response")

            hits_before = wrapped.cache_info().hits
            result = wrapped(*args, **kwargs)
            hits_after = wrapped.cache_info().hits

            if response:
                response.headers[cache_header] = (
                    "HIT" if hits_before < hits_after else "MISS"
                )

            return result

        wrapper.cache_info = wrapped.cache_info
        wrapper.cache_clear = wrapped.cache_clear
        wrapper.cache = wrapped.cache

        return wrapper

    return decorator


def clear_cache(func_name):
    """Clear cached for specific function. Useful for testing."""
    global _cache_store

    if cache := _cache_store.get(func_name):
        cache.clear()


def clear_all_cached():
    """Clear all cached stores. Useful for testing."""
    global _cache_store

    for cache in _cache_store.values():
        cache.clear()
