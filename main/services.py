from django.core.cache import cache

from mailing.settings import CACHE_ENABLED
from main.models import Client


def get_clients_from_cache():
    """Получаем клиентов из кэша, если кэш пуст, получаем данные из БД."""
    if not CACHE_ENABLED:
        return Client.objects.all()
    key = "client_list"
    clients = cache.get(key)
    if clients is not None:
        return clients
    clients = Client.objects.all()
    cache.set(key, clients)
    return clients


# def get_blogs_from_cache():
#     """Получаем посты из кэша, если кэш пуст, получаем данные из БД."""
#     if not CACHE_ENABLED:
#         return Blog.objects.all()
#     key = "blog_list"
#     blogs = cache.get(key)
#     if blogs is not None:
#         return blogs
#     blogs = Blog.objects.all()
#     cache.set(key, blogs)
#     return blogs
