"""
Перечень Django-signals приложения Service.
"""

from django.core.cache import cache
from django.db.models import QuerySet
from django.db.models.signals import post_save
from django.dispatch import receiver

from api.serializers import RatingSerializer
from cleanpro.app_data import REVIEW_CACHED_KEY
from services.models import Rating


def get_cached_reviews():
    """
    Возвращает кеши отзывов.
    """
    return cache.get(REVIEW_CACHED_KEY)


def update_cached_reviews():
    """
    Обновляет кэш отзывов.
    """
    reviews: QuerySet = Rating.objects.all()
    serializer = RatingSerializer(reviews, many=True)
    cache.set(REVIEW_CACHED_KEY, serializer.data)
    return


# TODO: надо также реализовать кэш на любое изменение объектов модели.
@receiver(signal=post_save, sender=Rating)
def post_save_receiver(sender, instance, created, **kwargs):
    """
    Получает сигнал post_save и направляет на соответствующий обработчик.
    """
    if isinstance(instance, Rating):
        update_cached_reviews()
    return
