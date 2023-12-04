"""
Команда для первичного импорта отзывов из Я.Карт.

Вызов команды осуществляется из папки с manage.py файлом:
python manage.ru init_parse_yandex_maps
"""

from django.core.management.base import BaseCommand

from services.tasks import parse_yandex_maps


class Command(BaseCommand):
    help = 'Loading services from csv.'

    def handle(self, *args: any, **options: any):
        parse_yandex_maps()
        return
