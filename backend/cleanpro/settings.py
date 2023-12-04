from datetime import timedelta
import os

from corsheaders.defaults import default_headers

from cleanpro.app_data import (
    BASE_DIR,
    CLEANPRO_HOST, CLEANPRO_HOST_IP,
    DEBUG, DEBUG_MAIL, DEBUG_DATABASE,
    DEFAULT_FROM_EMAIL,
    EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD,
    EMAIL_USE_TLS, EMAIL_USE_SSL, EMAIL_SSL_CERTFILE,
    EMAIL_SSL_KEYFILE, EMAIL_TIMEOUT,
    DATABASE_POSTGRESQL, DATABASE_SQLITE,
    SECRET_KEY,
    SOCIAL_AUTH_GITHUB_KEY, SOCIAL_AUTH_GITHUB_SECRET,
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY, SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
    SOCIAL_AUTH_VK_OAUTH2_KEY, SOCIAL_AUTH_VK_OAUTH2_SECRET,
    SOCIAL_AUTH_YANDEX_OAUTH2_KEY, SOCIAL_AUTH_YANDEX_OAUTH2_SECRET,
    SOCIAL_USER_PASSWORD_CYCLES,
)


"""App settings."""


DEBUG: bool = DEBUG


"""Celery settings."""


CELERY_TIMEZONE = 'Europe/Moscow'

CELERY_BEAT_SCHEDULE = {
    'parse_yandex_maps': {
        'task': 'services.tasks.parse_yandex_maps',
        'schedule': (
            timedelta(minutes=1) if DEBUG else
            timedelta(minutes=10)
        ),
    },
}

CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

CELERY_BROKER_URL = 'redis://cleanpro_redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://cleanpro_redis:6379/0'


"""Django settings."""


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://cleanpro_redis:6379/1',
    }
}

CACHE_TIMEOUT_SEC: int = 10 if DEBUG else 60 * 60 * 24

DATABASES = DATABASE_SQLITE if DEBUG_DATABASE else DATABASE_POSTGRESQL

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INSTALLED_APPS_DJANGO = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

INSTALLED_APPS_THIRD_PARTY = [
    'corsheaders',
    'django_filters',
    'django_password_validators',
    'djoser',
    'drf_spectacular',
    'phonenumber_field',
    'rest_framework',
    'rest_framework.authtoken',
    'social_django',
]

INSTALLED_APPS_LOCAL = [
    'api',
    'services',
    'users',
]

INSTALLED_APPS = INSTALLED_APPS_DJANGO + INSTALLED_APPS_THIRD_PARTY + INSTALLED_APPS_LOCAL

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# INFO: при использовании PostgreSQL рекомендуется использовать JSONB.
SOCIAL_AUTH_JSONFIELD_ENABLED = True

SPECTACULAR_SETTINGS = {
    "TITLE": "Cleanpro API",
    "VERSION": "0.5.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    "SCHEMA_PATH_PREFIX": r'/api/',
}

ROOT_URLCONF = 'cleanpro.urls'

WSGI_APPLICATION = 'cleanpro.wsgi.application'


"""Email settings."""


DEFAULT_FROM_EMAIL = DEFAULT_FROM_EMAIL

if DEBUG_MAIL:
    EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'sent_emails')
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST: str = EMAIL_HOST

EMAIL_PORT: int = EMAIL_PORT

EMAIL_HOST_USER: str = EMAIL_HOST_USER

EMAIL_HOST_PASSWORD: str = EMAIL_HOST_PASSWORD

if EMAIL_USE_TLS == 'True':
    EMAIL_USE_TLS: bool = True
else:
    EMAIL_USE_TLS: bool = False

if EMAIL_USE_SSL == 'True':
    EMAIL_USE_SSL: bool = True
else:
    EMAIL_USE_SSL: bool = False

if EMAIL_SSL_CERTFILE == 'None':
    EMAIL_SSL_CERTFILE: None = None

if EMAIL_SSL_KEYFILE == 'None':
    EMAIL_SSL_KEYFILE: None = None

EMAIL_TIMEOUT: int = EMAIL_TIMEOUT


"""Static files settings."""


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = 'media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_URL = 'static/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
            ],
        },
    },
]


"""Models data."""


ADMIN = 'admin'

ACCOUNT_EMAIL_REQUIRED = True

ACCOUNT_USER_MODEL_USERNAME_FIELD = None

ACCOUNT_USERNAME_REQUIRED = False

AUTH_USER_MODEL = 'users.User'

USER = 'user'


"""Regional settings."""


LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


"""Security settings."""


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.MinimumLengthValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.NumericPasswordValidator'
        ),
    },
    {
        'NAME': 'django_password_validators.password_character_requirements.password_validation.PasswordCharacterValidator'
    },
]

AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    # https://developers.google.com/identity/protocols/oauth2?csw=1&hl=ru
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.yandex.YandexOAuth2',
    # https://dev.vk.com/ru/method
    'social_core.backends.vk.VKAppOAuth2',
    # INFO: ModelBackend должен идти последним.
    # INFO: нужен, если используется django.contrib.auth в проекте.
    'django.contrib.auth.backends.ModelBackend',
)

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    CLEANPRO_HOST,
    CLEANPRO_HOST_IP,
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    *default_headers,
    "access-control-allow-credentials",
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1',
    f'https://{CLEANPRO_HOST}'
]

CSRF_TRUSTED_ORIGINS = [
    f'https://{CLEANPRO_HOST}',
]

DJOSER = {
    'SERIALIZERS': {
        'user': 'api.serializers.UserSerializer',
    }
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # INFO: следующие 2 строки устанавливают кеширование данных по GET запросу.
    #       Данный вопрос пока на проработке.
    # 'django.middleware.cache.UpdateCacheMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
]

SECRET_KEY: str = SECRET_KEY

SOCIAL_AUTH_GITHUB_KEY: str = SOCIAL_AUTH_GITHUB_KEY
SOCIAL_AUTH_GITHUB_SECRET: str = SOCIAL_AUTH_GITHUB_SECRET

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY: str = SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET: str = SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET
SOCIAL_AUTH_VK_OAUTH2_KEY: str = SOCIAL_AUTH_VK_OAUTH2_KEY
SOCIAL_AUTH_VK_OAUTH2_SECRET: str = SOCIAL_AUTH_VK_OAUTH2_SECRET
SOCIAL_AUTH_YANDEX_OAUTH2_KEY: str = SOCIAL_AUTH_YANDEX_OAUTH2_KEY
SOCIAL_AUTH_YANDEX_OAUTH2_SECRET: str = SOCIAL_AUTH_YANDEX_OAUTH2_SECRET

SOCIAL_AUTH_PIPELINE = (
    # Get the information we can about the user and return it in a simple
    # format to create the user instance later.
    'social_core.pipeline.social_auth.social_details',
    # Get the social uid from whichever service we're authing thru.
    # The uid is the unique identifier of the given user in the provider.
    'social_core.pipeline.social_auth.social_uid',
    # Verifies that the current auth process is valid
    # within the current project, this is where emails and domains
    # whitelists are applied (if defined).
    'social_core.pipeline.social_auth.auth_allowed',
    # CUSTOM create a user account if does'n exists.
    'users.oauth.create_user_social_pipeline',
)

# # Path to redirect if new user oauth succeed.
SOCIAL_AUTH_LOGIN_REDIRECT_URL: str = '/'

SOCIAL_USER_FIELDS: tuple[str] = (
    'first_name',
    'last_name',
    'email',
)

SOCIAL_USER_PASSWORD_CYCLES: int = SOCIAL_USER_PASSWORD_CYCLES
