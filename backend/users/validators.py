import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext

EMAIL_PATTERN: str = r'^(?!\.)[0-9A-Za-z\.]{5,50}@[a-zA-z]+\.[a-zA-z]+$'
EMAIL_ERROR: str = gettext(
    'Введите корректный email (например: example@example.ru)'
)
USERNAME_PATTERN: str = r'^[А-ЯЁа-яё][А-ЯЁа-яё\s\-]{1,28}[А-ЯЁа-яё]$'
USERNAME_ERROR: str = gettext(
    'Укажите корректное имя '
    '(например: Апполинарий Вальдемарович фон Спасо-Преображенский)'
)
PASS_PATTERN: str = (
    r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!_@#$%^&+=]).{5,50}$'
)
PASS_ERROR: str = gettext(
    'Введите пароль, который удовлетворяет критериям:\n'
    '    - длина от 5 до 50 символов;\n'
    '    - включает хотя бы одну цифру (0-9);\n'
    '    - включает хотя бы одну прописную букву (a-z);\n'
    '    - включает хотя бы одну заглавную букву (A-Z);\n'
    '    - включает хотя бы один специальный символ (!_@#$%^&+=).'
)


def validate_password(value):
    """Производит валидацию поля модели для пароля."""
    if re.fullmatch(PASS_PATTERN, value):
        return value
    raise ValidationError(PASS_ERROR)


def validate_username(value):
    """Производит валидацию поля модели для имени."""
    """Производит валидацию поля модели для имени."""
    if re.fullmatch(USERNAME_PATTERN, value):
        return value
    raise ValidationError(USERNAME_ERROR)


def validate_email(value):
    """Производит валидацию поля модели для почты."""
    if re.fullmatch(EMAIL_PATTERN, value):
        return value
    raise ValidationError(EMAIL_ERROR)
