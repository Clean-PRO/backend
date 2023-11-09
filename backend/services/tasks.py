"""
Список задач для Celery.
"""

from datetime import datetime, timedelta
import requests

from bs4 import BeautifulSoup
from bs4.element import Tag, ResultSet
from celery import shared_task
from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from rest_framework import status

from cleanpro.app_data import CLEANPRO_YA_MAPS_URL
from services.models import Rating
from services.signals import update_cached_reviews


@shared_task
def parse_yandex_maps():
    response: requests = requests.get(CLEANPRO_YA_MAPS_URL)
    if not response.status_code == status.HTTP_200_OK:
        raise Exception(
            f'Указан неверный URL отзыва: "{CLEANPRO_YA_MAPS_URL}"'
        )
    soup: BeautifulSoup = BeautifulSoup(response.text, features="html.parser")
    if not soup:
        raise Exception('Отзывы отсутствуют.')
    all_comment_elements: ResultSet = soup.find_all('div', class_='comment')
    all_comments: QuerySet = Rating.objects.all()
    new_comments: list[Rating] = []
    for comment in all_comment_elements:
        text: str = comment.find('p', class_='comment__text').text.strip()
        if all_comments.filter(text=text).exists():
            break
        username: str = comment.find('p', class_='comment__name').text.strip()
        stars_ul: Tag = comment.find('ul', class_='stars-list')
        stars: ResultSet = stars_ul.find_all('li', class_='stars-list__star')
        full_stars: list[Tag] = [
            star for star in stars if
            '_empty' not in star.get('class') and
            '_half' not in star.get('class')
        ]
        try:
            new_comments.append(
                Rating(
                    username=username,
                    from_maps=True,
                    # INFO: на картах просто указывается что-то вроде
                    #       "1 января" без указания года. Чтобы не
                    #       усложнять логику - данная задача запускается
                    #       разв сутки в 00:00 (UTC+3) и записывает
                    #       "вчерашние" отзывы.
                    pub_date=datetime.now() - timedelta(days=1),
                    text=text,
                    score=len(full_stars),
                )
            )
        except ValidationError:
            continue
    if new_comments:
        Rating.objects.bulk_create(new_comments)
        update_cached_reviews()
    return
