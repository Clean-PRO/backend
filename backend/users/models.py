# TODO: при релизе проверить, что валидация на клиенте
#       совпадает с валидацией на сервере!

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from cleanpro.app_data import (
    ADDRESS_CITY_MAX_LEN, ADDRESS_STREET_MAX_LEN, ADDRESS_HOUSE_MAX_VAL,
    ADDRESS_ENTRANCE_MAX_VAL, ADDRESS_FLOOR_MAX_VAL, ADDRESS_APARTMENT_MAX_VAL,
    USER_NAME_MAX_LEN, USER_PASS_MAX_LEN,
    USER_FULL_EMAIL_MAX_LEN,
)
from users.validators import (
    validate_email, validate_username, validate_password
)


class Address(models.Model):
    """Модель адреса."""

    city = models.CharField(
        verbose_name='Город',
        max_length=ADDRESS_CITY_MAX_LEN
    )
    street = models.CharField(
        verbose_name='Улица',
        max_length=ADDRESS_STREET_MAX_LEN
    )
    house = models.PositiveSmallIntegerField(
        verbose_name='Дом',
        validators=[
            MaxValueValidator(
                ADDRESS_HOUSE_MAX_VAL,
                'Укажите корректный номер дома.',
            )
        ]
    )
    entrance = models.IntegerField(
        verbose_name='Подъезд',
        validators=[
            MaxValueValidator(
                ADDRESS_ENTRANCE_MAX_VAL,
                'Укажите корректный подъезд.',
            )
        ],
        null=True,
        blank=True,
    )
    floor = models.IntegerField(
        verbose_name='Этаж',
        validators=[
            MaxValueValidator(
                ADDRESS_FLOOR_MAX_VAL,
                'Укажите корректный этаж.',
            )
        ],
        null=True,
        blank=True,
    )
    apartment = models.IntegerField(
        verbose_name='Квартира',
        validators=[
            MaxValueValidator(
                ADDRESS_APARTMENT_MAX_VAL,
                'Укажите корректный номер квартиры.'
            )
        ],
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'
        ordering = (
            'city',
            'street',
            'house',
            'entrance',
            'floor',
            'apartment',
        )


class UserManager(BaseUserManager):
    """Менеджер модели пользователя."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Создает и сохраняет пользователя с полученными почтой и паролем."""
        if not email or not password:
            raise ValueError('Укажите email и password.')
        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        """Обрабатывает метод создания пользователя."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Обрабатывает метод создания пользователя-администратора."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)

    def create_cleaner(self, email, password, **extra_fields):
        """Обрабатывает метод создания пользователя-уборщика."""
        extra_fields.setdefault('is_cleaner', True)
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Модель пользователя."""

    # TODO: добавить фото.
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=USER_NAME_MAX_LEN,
        validators=(validate_username,),
        blank=True,
        null=True,
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=USER_FULL_EMAIL_MAX_LEN,
        validators=(validate_email,),
        unique=True,
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=USER_PASS_MAX_LEN,
        validators=(validate_password,),
    )
    phone = PhoneNumberField(
        verbose_name='Номер телефона',
        region='RU',
        blank=True,
        null=True,
    )
    address = models.ForeignKey(
        Address,
        verbose_name='Адрес',
        related_name='users',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    # INFO: следующие 3 атрибута нужны для учетной записи уборщиков.
    is_cleaner = models.BooleanField(
        verbose_name='Уборщик',
        default=False,
    )
    # TODO: написать задачу для Celery, которая бы после достижения
    #       окончания отпуска обнуляла эти 2 поля.
    on_vacation_from = models.DateField(
        verbose_name='Начало отпуска',
        default=None,
        blank=True,
        null=True,
    )
    on_vacation_to = models.DateField(
        verbose_name='Конец отпуска',
        default=None,
        blank=True,
        null=True,
    )

    objects = UserManager()
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('email',)

    def __str__(self):
        return self.email
