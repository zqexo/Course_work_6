from django.core.cache import cache

from blog.models import Blog
from mailing.settings import CACHE_ENABLED


def get_blogs_from_cache():
    """Получаем посты из кэша, если кэш пуст, получаем данные из БД."""
    if not CACHE_ENABLED:
        return Blog.objects.all()
    key = "blog_list"
    blogs = cache.get(key)
    if blogs is not None:
        return blogs
    blogs = Blog.objects.all()
    cache.set(key, blogs)
    return blogs
