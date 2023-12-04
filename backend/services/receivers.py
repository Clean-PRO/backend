from django.core.cache import cache
from django.db.models.signals import post_delete
from django.dispatch import receiver

from cleanpro.app_data import CACHE_LIST_RESPONSE_RATINGS
from services.models import Rating


@receiver(signal=post_delete, sender=Rating)
def delete_cache_rating(*args, **kwargs) -> None:
    """Удаляет кэш для отзывов при удалении объекта модели Rating"""
    cache.delete(CACHE_LIST_RESPONSE_RATINGS)
    return
