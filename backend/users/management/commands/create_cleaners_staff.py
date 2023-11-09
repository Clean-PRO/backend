"""
Команда для создания объектов уборщиков модели User

Вызов команды осуществляется из папки с manage.py файлом:
python manage.ru create_cleaners_staff
"""

from django.db.models import QuerySet
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError

from api.utils import create_password
from users.models import User

CLEANERS_MIN: int = 2
CLEANERS_MAX: int = 9

NUMS_TO_TEXT: dict[int, str] = {
    1: 'Первый',
    2: 'Второй',
    3: 'Третий',
    4: 'Четвертый',
    5: 'Пятый',
    6: 'Шестой',
    7: 'Седьмой',
    8: 'Восьмой',
    9: 'Девятый',
}


def create_cleaners(count: int) -> None:
    """Создает указанное количество уборщиков."""
    if count not in range(CLEANERS_MIN, CLEANERS_MAX+1):
        count: int = CLEANERS_MIN
    cleaners_exists: QuerySet = User.objects.filter(is_cleaner=True)
    new_cleaners: list[User] = []
    for i in range(1, count+1):
        try:
            email: str = f'cleaner_pro_{i}@email.com'
            if cleaners_exists.filter(email=email).exists():
                continue
            password: str = create_password(email=email)
            username: str = f'Иван Клинер-{NUMS_TO_TEXT.get(i, "Неизвестный")}'
            new_cleaner: User = User(
                email=email,
                username=username,
                is_cleaner=True,
                phone=f'+7 911 222-22-0{i}'
            )
            new_cleaner.set_password(password)
            new_cleaners.append(new_cleaner)
        except ValidationError as err:
            # TODO: Подключить логгер
            print(f'Уборщик №{i} не был добавлен: {err}')
    User.objects.bulk_create(new_cleaners)
    return


class Command(BaseCommand):
    help = 'Create cleaners.'

    def handle(self, *args: any, **options: any):
        CLEANERS_TO_CREATE_COUNT: int = 5
        try:
            create_cleaners(count=CLEANERS_TO_CREATE_COUNT)
        except Exception as err:
            raise CommandError(f'Exception has occurred: {err}')
        return
