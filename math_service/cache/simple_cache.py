# Usage of dictionary to avoid results recomputing

cache_store = {}


def get_from_cache(key: str):
    return cache_store.get(key)


def set_to_cache(key: str, value):
    cache_store[key] = value
