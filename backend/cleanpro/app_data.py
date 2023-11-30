import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR, '.env'), verbose=True)


"""Company data."""


CLEANPRO_HOST: str = os.getenv('CLEANPRO_HOST')
CLEANPRO_HOST_IP: str = os.getenv('CLEANPRO_HOST_IP')

CLEANPRO_YA_MAPS_ID: str = os.getenv('CLEANPRO_YA_MAPS_ID')

CLEANPRO_YA_MAPS_URL: str = (
    f'https://yandex.ru/maps-reviews-widget/{CLEANPRO_YA_MAPS_ID}?comments'
)

SCHEDULE_WORK_START_H: str = 9
SCHEDULE_WORK_STOP_H: str = 21


"""Database settings."""


DB_ENGINE: str = os.getenv('DB_ENGINE')
DB_HOST: str = os.getenv('DB_HOST')
DB_PORT: str = os.getenv('DB_PORT')
DB_NAME: str = os.getenv('POSTGRES_DB')
DB_USER: str = os.getenv('POSTGRES_USER')
DB_PASSWORD: str = os.getenv('POSTGRES_PASSWORD')

DATABASE_POSTGRESQL: dict[str, dict[str, any]] = {
    'default': {
        'ENGINE': DB_ENGINE,
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}

DATABASE_SQLITE: dict[str, dict[str, any]] = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


"""Debug settings."""


DEBUG: str = os.getenv('DEBUG')
if DEBUG == 'True':
    DEBUG: bool = True
else:
    DEBUG: bool = False

DEBUG_DATABASE: str = os.getenv('DEBUG_DATABASE')
if DEBUG_DATABASE == 'True':
    DEBUG_DATABASE: bool = True
else:
    DEBUG_DATABASE: bool = False

DEBUG_MAIL: str = os.getenv('DEBUG_MAIL')
if DEBUG_MAIL == 'True':
    DEBUG_MAIL: bool = True
else:
    DEBUG_MAIL: bool = False


"""Models data."""


ADMIN_LIST_PER_PAGE: int = 15

ADDRESS_CITY_MAX_LEN: int = 50
ADDRESS_STREET_MAX_LEN: int = 50
ADDRESS_HOUSE_MAX_VAL: int = 999
ADDRESS_ENTRANCE_MAX_VAL: int = 50
ADDRESS_FLOOR_MAX_VAL: int = 150
ADDRESS_APARTMENT_MAX_VAL: int = 9999

CLEANING_TIME_MINUTE_MIN: int = 1

CLEANING_TYPE_TITLE_MAX_LEN: int = 25
CLEANING_TYPE_COEF_MIN_VAL: int = 1

MEASURE_TITLE_MAX_LEN: int = 25

ORDER_ACCEPTED_STATUS: str = 'accepted'
ORDER_CANCELLED_STATUS: str = 'cancelled'
ORDER_CREATED_STATUS: str = 'created'
ORDER_FINISHED_STATUS: str = 'finished'
ORDER_STATUS_CHOICES: list[tuple[str]] = (
    (ORDER_CREATED_STATUS, 'Создан'),
    (ORDER_ACCEPTED_STATUS, 'Принят'),
    (ORDER_FINISHED_STATUS, 'Завершен'),
    (ORDER_CANCELLED_STATUS, 'Отменен'),
)
ORDER_COMMENT_MAX_LEN: int = 512
ORDER_TOTAL_SUM_MIN_VAL: int = 1
ORDER_TOTAL_TIME_MIN_VAL: int = 1

REVIEW_CACHED_KEY: str = 'review_cached_key'

SERVICES_ADDITIONAL: str = 'additional'
SERVICES_MAIN: str = 'main'
SERVICE_TYPE: list[tuple[str]] = [
    (SERVICES_MAIN, 'Основная'),
    (SERVICES_ADDITIONAL, 'Дополнительная'),
]
SERVICE_TYPE_MAX_LEN: int = 11
SERVICE_PRICE_MIN_VAL: int = 60
SERVICE_TITLE_MAX_LEN: int = 60

USER_NAME_MAX_LEN: int = 30
# Do not change, Django hash password with big length!
USER_PASS_MAX_LEN: int = 512
# Minimum 2 cycles are required!
USER_PASS_RAND_CYCLES: int = 2
USER_FULL_EMAIL_MAX_LEN: int = 80


"""Email data."""


EMAIL_CODE_LENGTH: int = 8

DEFAULT_FROM_EMAIL: str = os.getenv('DEFAULT_FROM_EMAIL')

PASSWORD_RESET_LINK: str = None

EMAIL_CONFIRM_EMAIL_SUBJECT: str = 'Подтверждение почты | CleanPro'

EMAIL_CONFIRM_EMAIL_TEXT: str = (
    'Добро пожаловать в Cleanpro!'
    '\n\n'
    'Наша команда специалистов готова предложить '
    'высококачественные клининговые услуги, которые сделают '
    'ваше пространство сияюще чистым и ухоженным.'
    '\n\n'
    'Для подтверждения электронной почты пожалуйста введите '
    'в появившемся окне на сайте пароль учетной записи, указанный ниже:'
    '\n\n'
    '{password}'
    '\n\n'
    'В целях безопасности рекомендуем вас сменить пароль в личном кабинете.'
    '\n\n'
    'С наилучшими пожеланиями,\n'
    'Команда CleanPro'
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


"""Email settings."""


EMAIL_HOST: str = os.getenv('EMAIL_HOST')

EMAIL_PORT: str = os.getenv('EMAIL_PORT')

EMAIL_HOST_USER: str = os.getenv('EMAIL_HOST_USER')

EMAIL_HOST_PASSWORD: str = os.getenv('EMAIL_HOST_PASSWORD')

EMAIL_USE_TLS: str = os.getenv('EMAIL_USE_TLS', False)

EMAIL_USE_SSL: str = os.getenv('EMAIL_USE_SSL', False)

EMAIL_SSL_CERTFILE: str = os.getenv('EMAIL_SSL_CERTFILE', 'None')

EMAIL_SSL_KEYFILE: str = os.getenv('EMAIL_SSL_KEYFILE', 'None')

EMAIL_TIMEOUT: int = os.getenv('EMAIL_TIMEOUT')
if EMAIL_TIMEOUT is not None:
    EMAIL_TIMEOUT: int = int(EMAIL_TIMEOUT)


"""Security data."""


SECRET_KEY: str = os.getenv('SECRET_KEY')

SECRET_SALT: str = os.getenv('SECRET_SALT')

PASS_ITERATIONS: int = os.getenv('PASS_ITERATIONS')
if PASS_ITERATIONS is not None:
    PASS_ITERATIONS: int = int(PASS_ITERATIONS)


"""Social Auth."""

SOCIAL_AUTH_GITHUB_KEY = os.getenv('SOCIAL_AUTH_GITHUB_KEY')
SOCIAL_AUTH_GITHUB_SECRET = os.getenv('SOCIAL_AUTH_GITHUB_SECRET')
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')  # noqa (E501)
SOCIAL_AUTH_VK_OAUTH2_KEY = os.getenv('SOCIAL_AUTH_VK_OAUTH2_KEY')
SOCIAL_AUTH_VK_OAUTH2_SECRET = os.getenv('SOCIAL_AUTH_VK_OAUTH2_SECRET')
SOCIAL_AUTH_YANDEX_OAUTH2_KEY = os.getenv('SOCIAL_AUTH_YANDEX_OAUTH2_KEY')
SOCIAL_AUTH_YANDEX_OAUTH2_SECRET = os.getenv('SOCIAL_AUTH_YANDEX_OAUTH2_SECRET')  # noqa (E501)

SOCIAL_USER_PASSWORD_CYCLES: int = 50
