from django.core.cache import cache


def hit(key: str, limit: int, window_seconds: int) -> bool:
    """
    Returns True if allowed, False if blocked.
    Cache-based, works with LocMem in dev; Redis-ready later.
    """
    cache_key = f"rl:{key}"
    count = cache.get(cache_key, 0)

    if count >= limit:
        return False

    if count == 0:
        cache.set(cache_key, 1, timeout=window_seconds)
    else:
        cache.incr(cache_key)

    return True