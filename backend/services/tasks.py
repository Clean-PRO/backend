"""
Список задач для Celery.
"""

from datetime import datetime
import requests

from bs4 import BeautifulSoup
from bs4.element import Tag, ResultSet
from celery import shared_task
from django.core.cache import cache
from django.core.exceptions import ValidationError
from rest_framework import status

from cleanpro.app_data import CACHE_LIST_RESPONSE_RATINGS, CLEANPRO_YA_MAPS_URL
from services.models import Rating


@shared_task
def parse_yandex_maps():
    response: requests = requests.get(CLEANPRO_YA_MAPS_URL)
    if not response.status_code == status.HTTP_200_OK:
        raise Exception(
            f'Указан невалидный URL: "{CLEANPRO_YA_MAPS_URL}"'
        )
    soup: BeautifulSoup = BeautifulSoup(response.text, features='html.parser')
    if not soup.find():
        raise Exception('Отзывы отсутствуют.')
    all_comment_elements: ResultSet = soup.find_all('div', class_='comment')
    last_comment: Rating = (
        Rating.objects.filter(from_maps=True).order_by('-id').first()
    )
    if last_comment:
        last_comment_text: str = last_comment.text
        # INFO: в Я.Картах отзывы сортируются от новых к старым.
        #       Если отзывы с Я.Карт не были импортированы, их надо в первый
        #       раз загрузить/прочитать в обратном порядке (-1).
        direction: int = 1
    else:
        last_comment_text: None = None
        direction: int = -1
    new_comments: list[Rating] = []
    time_now: datetime = datetime.now()
    for comment in all_comment_elements[::direction]:
        text: str = comment.find('p', class_='comment__text').text.strip()
        if text == last_comment_text:
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
                    pub_date=time_now,
                    text=text,
                    score=len(full_stars),
                )
            )
        except ValidationError:
            continue
    if new_comments:
        Rating.objects.bulk_create(new_comments)
        cache.delete(CACHE_LIST_RESPONSE_RATINGS)
    return
