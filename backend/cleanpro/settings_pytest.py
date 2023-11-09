from cleanpro.app_data import DATABASE_SQLITE
from cleanpro.settings import *  # noqa F403

DATABASES = DATABASE_SQLITE

SECRET_KEY = 'test_secret_key'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media_test')  # noqa F405
