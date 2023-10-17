"""
Команда для импорта объектов модели ServicesInCleaningType из csv файла:
services/management/commands/csv_import/cleaning_types/cleaning_types.csv

Важно! Предварительно необходимо создать соответствующие объекты
модели Service в базе данных!

Вызов команды осуществляется из папки с manage.py файлом:
python manage.ru csv_cleaning_types_import
"""

import csv
from typing import Optional

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import QuerySet

from services.models import CleaningType, Service, ServicesInCleaningType


import_path: str = 'services/management/commands/csv_import/cleaning_types/'

cleaning_types_data: list[CleaningType] = []
cleaning_types_titles: list[str] = list(
    [title[0] for title in CleaningType.objects.values_list('title')]
)
services: QuerySet = Service.objects.all()
services_dict = {service.title: service for service in services}


class BrokenServicesException(Exception):
    """Ошибка создания в базе данных объектов модели Services."""
    def __init__(self, message):
        super().__init__(message)


class ServicesIsEmptyException(Exception):
    """Ошибка отсутствия в базе данных объектов модели Services."""
    def __init__(self, message='No single Service object exists. Skip task.'):
        super().__init__(message)


def check_if_services_exists() -> None:
    """Вызывает ServicesIsEmptyException, если не существует
    ни одного объекта модели Services. Иначе - возвращает None."""
    if not services.exists():
        raise ServicesIsEmptyException
    return None


def create_services_in_cleaning_types(
        cleaning_type: CleaningType,
        services_titles: list[str]
        ) -> Optional[list[str]]: # noqa E126
    """Создает объекты модели ServicesInCleaningType.
    Возвращает None в случае успеха (нет отсутствующих сервисов).
    Возвращает список наименований сервисов в случае,
    если они отсутствуют в базе данных."""
    services_in_cleaning_types: list[ServicesInCleaningType] = []
    broken_services: list[str] = []
    for title in services_titles:
        service: Service = services_dict.get(title)
        if service:
            services_in_cleaning_types.append(
                ServicesInCleaningType(
                    cleaning_type=cleaning_type,
                    service=service,
                )
            )
        else:
            broken_services.append(title)
    if broken_services:
        return broken_services
    ServicesInCleaningType.objects.bulk_create(services_in_cleaning_types)
    return None


def get_cleaning_type_data(
        data: dict
        ) -> Optional[tuple[str, float, list[str]]]:  # noqa E126
    """Проверяет наличие необходимых данных для создания объекта модели
    CleaningType приводит их нужным Python типам и возвращает в следующем
    порядке: title, coefficient, type, services_titles.
    Не возвращает ничего, если данные отсутствуют или объект модели
    CleaningType с заданным полем title уже существует."""
    title: str = data.get('title')
    if not title or title in cleaning_types_titles:
        return
    coefficient: str = data.get('coefficient')
    services_titles: str = data.get('services')
    if not all((coefficient, services_titles)):
        return None
    return title, float(coefficient), services_titles.split('/')


@transaction.atomic
def create_cleaning_type_object(data: dict) -> Optional[CleaningType]:
    """Создает и возвращает объект модели CleaningType в случае сообщения
    валидных данных данных. Иначе - возвращает None."""
    cleaning_type_data: Optional[tuple[str, float, str, list[str]]] = (
        get_cleaning_type_data(data=data)
    )
    if cleaning_type_data is None:
        return None
    title, coefficient, services_titles = cleaning_type_data
    # TODO: посмотреть за безопасностью создания объектов в БД
    cleaning_type: CleaningType = CleaningType.objects.create(
        title=title,
        coefficient=coefficient,
    )
    broken_services = create_services_in_cleaning_types(
        cleaning_type=cleaning_type,
        services_titles=services_titles,
    )
    if broken_services:
        cleaning_type.delete()
        raise BrokenServicesException(
            f'Can not create "{title}" because some services do not exist: '
            f'{", ".join(broken_services)}'
        )
    return None


def read_csv(full_path: str) -> list[dict]:
    """Читает CSV-файл и возвращает его содержимое в виде списка словарей.
    Если файл не существует - вызывает FileNotFoundError."""
    # TODO: подумать в сторону аннотации, как в Python объектах:
    """
    Читает CSV-файл и возвращает его содержимое в виде списка словарей.

    Args:
        full_path (str): путь к CSV-файлу.

    Returns:
        list[dict]: список словарей, представляющих строки CSV-файла.

    Raises:
        FileNotFoundError: если файл не существует.
    """
    # TODO подумать над закрытием файла. Выдает ошибку последующего чтения.
    reader_data: list[dict] = []
    try:
        with open(full_path, mode='r', encoding='utf-8') as file:
            reader: csv.DictReader = csv.DictReader(file, delimiter=';')
            for row in reader:
                reader_data.append(row)
    except FileNotFoundError:
        raise FileNotFoundError(
            f'File "{full_path}" is not provided. Abort task.'
        )
    return reader_data


class Command(BaseCommand):
    help = 'Loading cleaning types from csv.'

    def handle(self, *args: any, **options: any):
        file_path: str = f'{import_path}cleaning_types.csv'
        check_if_services_exists()
        csv_file: list[dict] = read_csv(full_path=file_path)
        # TODO: подключить логгер на перехватах ошибок.
        for row in csv_file:
            try:
                create_cleaning_type_object(data=row)
            except BrokenServicesException as err:
                print(err)
            except Exception as err:
                raise CommandError(f'Exception has occurred: {err}')
        return
