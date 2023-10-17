import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR, '.env'), verbose=True)


"""Company data."""


CLEANPRO_HOST = os.getenv('CLEANPRO_HOST')

CLEANPRO_YA_MAPS_ID: str = os.getenv('CLEANPRO_YA_MAPS_ID')

CLEANPRO_YA_MAPS_URL: str = (
    f'https://yandex.ru/maps-reviews-widget/{CLEANPRO_YA_MAPS_ID}?comments'
)

SCHEDULE_WORK_START_H: str = 9
SCHEDULE_WORK_STOP_H: str = 21

HOURS_IN_DAY: int = 24
AVAILABLE_MINUTES: tuple[int] = (0, 30)


def schedule_generate_bool(value: any = False):
    """
    Генерирует пустой словарь с графиком времени уборок.
    Формат: {"00:00": value, "00:30": value, ... "23:30": value}
    """
    schedule_bool: dict[str, any] = {}
    for hour in range(HOURS_IN_DAY):
        for minute in AVAILABLE_MINUTES:
            schedule_bool[f'{hour:02}:{minute:02}'] = value
    return schedule_bool


"""Database settings."""


DB_ENGINE = os.getenv('DB_ENGINE')
DB_USER = os.getenv('POSTGRES_USER')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('POSTGRES_DB')


"""Models data."""


ADMIN_LIST_PER_PAGE: int = 15

ORDER_CANCELLED_STATUS: str = 'cancelled'

REVIEW_CACHED_KEY: str = 'review_cached_key'


"""Email data."""

EMAIL_CODE_LENGTH: int = 8

DEFAULT_FROM_EMAIL: str = 'cleanpronew2023@gmail.com'

PASSWORD_RESET_LINK: str = None

EMAIL_CONFIRM_CODE_SUBJECT: str = 'Confirm email | CleanPro'

EMAIL_CONFIRM_CODE_TEXT: str = (
    'Hello there!\n'
    '\n'
    'Thank You for you ordering!'
    '\n'
    'To confirm your email please enter the code below into the cite.\n'
    '\n'
    '{confirm_code}\n'
    '\n'
    'Best regards,\n'
    'The CleanPro Team'
)

EMAIL_REGISTER_SUBJECT: str = 'Welcome to CleanPro!'

EMAIL_REGISTER_TEXT: str = (
    'Hello there!\n'
    '\n'
    'Welcome to CleanPro! We are thrilled to have You as part '
    'of our community.\n'
    '\n'
    'If You want to (re)set your password, You can do it by following link:  '
    f'{PASSWORD_RESET_LINK}''\n'
    '\n'
    'If You have any questions or need further assistance, do not hesitate '
    f'to reach out to us at {DEFAULT_FROM_EMAIL}.''\n'
    '\n'
    'Thank You for choosing CleanPro! We hope You will enjoy your time with '
    'us and wish You a pleasant experience.\n'
    '\n'
    'Best regards,\n'
    'The CleanPro Team'
)
