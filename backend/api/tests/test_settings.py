import os

from cleanpro.app_data import (
    # Secrets
    PASS_ITERATIONS, SECRET_KEY, SECRET_SALT,
    # Company data
    CLEANPRO_HOST, CLEANPRO_HOST_IP, CLEANPRO_YA_MAPS_ID,
    # Database settings
    DATABASE_POSTGRESQL, DB_ENGINE, DB_HOST,
    DB_NAME, DB_PASSWORD, DB_PORT, DB_USER,
    # Email SMTP-server settings
    DEFAULT_FROM_EMAIL, EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER,
    EMAIL_HOST_PASSWORD, EMAIL_USE_TLS, EMAIL_USE_SSL, EMAIL_SSL_CERTFILE,
    EMAIL_SSL_KEYFILE, EMAIL_TIMEOUT,
)
from cleanpro.settings import BASE_DIR, DATABASES, DEBUG


class TestProdSettings():
    """Производит тест настроек проекта перед деплоем на сервер."""

    def test_db_is_postgresql(self) -> None:
        """Проверяет, что база данных проекта: PostgreSQL."""
        assert DATABASES == DATABASE_POSTGRESQL, (
            'Установите для settings.DATABASES '
            'значение cleanpro.app_data.DATABASE_POSTGRESQL.'
        )
        return

    def test_debug_is_false(self) -> None:
        """Проверяет, что DEBUG=False."""
        assert not DEBUG, 'Установите для settings.DEBUG значение False.'
        return

    def test_env(self) -> None:
        """
        Проверяет, что в проекте существует .env файл,
        который содержит все необходимые поля.
        """
        env_file_path = os.path.join(BASE_DIR, '.env')
        assert os.path.isfile(env_file_path), 'Создайте .env файл.'
        missed_fields: list[str] = []
        ENV_DATA: dict[str, any] = {
            # Secrets
            'SECRET_KEY': SECRET_KEY,
            'SECRET_SALT': SECRET_SALT,
            'PASS_ITERATIONS': PASS_ITERATIONS,
            # Company data
            'CLEANPRO_HOST': CLEANPRO_HOST,
            'CLEANPRO_YA_MAPS_ID': CLEANPRO_YA_MAPS_ID,
            'CLEANPRO_HOST_IP': CLEANPRO_HOST_IP,
            # Database settings
            'DB_ENGINE': DB_ENGINE,
            'DB_HOST': DB_HOST,
            'DB_PORT': DB_PORT,
            'DB_NAME': DB_NAME,
            'DB_USER': DB_USER,
            'DB_PASSWORD': DB_PASSWORD,
            # Email SMTP-server settings
            'DEFAULT_FROM_EMAIL': DEFAULT_FROM_EMAIL,
            'EMAIL_HOST': EMAIL_HOST,
            'EMAIL_PORT': EMAIL_PORT,
            'EMAIL_HOST_USER': EMAIL_HOST_USER,
            'EMAIL_HOST_PASSWORD': EMAIL_HOST_PASSWORD,
            'EMAIL_USE_TLS': EMAIL_USE_TLS,
            'EMAIL_USE_SSL': EMAIL_USE_SSL,
            'EMAIL_SSL_CERTFILE': EMAIL_SSL_CERTFILE,
            'EMAIL_SSL_KEYFILE': EMAIL_SSL_KEYFILE,
            'EMAIL_TIMEOUT': EMAIL_TIMEOUT,
        }
        for key, value in ENV_DATA.items():
            if value is None:
                missed_fields.append(key)
        assert not missed_fields, (
            'В .env файле отсутствуют следующие поля: '
            f'{", ".join(field for field in missed_fields)}'
        )
        return
