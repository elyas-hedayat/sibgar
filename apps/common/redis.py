from django.core.cache import cache
from django.conf import settings


def add_to_cache(id: str, mode, value: str | dict, ttl: int = settings.CACHE_TTL) -> dict:
    name = f'{id}_{mode.lower()}'
    cached_data = cache.set(name=name, value=value, timeout=ttl)
    return cached_data


def delete_from_cache(id, mode):
    name = f'{id}_{mode.lower()}'
    cache.delete(name)


def get_from_cache(id, mode):
    name = f'{id}_{mode.lower()}'
    return cache.get(name=name)
