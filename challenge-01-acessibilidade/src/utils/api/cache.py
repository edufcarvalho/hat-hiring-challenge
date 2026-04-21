import time
from functools import wraps
from typing import Any, Callable, Optional, Type

_cache_store: dict = {}


def cache(
    expire: Optional[int] = None,
    coder: Optional[Type] = None,
    key_builder: Optional[Callable] = None,
    namespace: str = "",
    injected_dependency_namespace: str = "__fastapi_cache",
    cache_header: str = "X-Cache",
) -> Callable:
    """
    Simple cache decorator that adds cache status header (HIT/MISS).
    Each decorated function gets its own cache entry.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func_id = id(func)

        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            response = kwargs.get("response")
            cached = _cache_store.get(func_id)

            is_expired = (
                expire and time.time() > cached.get("expire_at", 0) if cached else True
            )

            if cached is None or is_expired:
                _cache_store[func_id] = {
                    "result": func(*args, **kwargs),
                    "expire_at": time.time() + expire if expire else float("inf"),
                }
                if response:
                    response.headers[cache_header] = "MISS"
                return _cache_store[func_id]["result"]

            if response:
                response.headers[cache_header] = "HIT"
            return cached["result"]

        return wrapper

    return decorator


def clear_cache():
    """Clear all cached data. Useful for testing."""
    _cache_store.clear()
