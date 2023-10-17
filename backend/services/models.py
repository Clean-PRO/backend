# TODO: при релизе проверить, что валидация на клиенте
#       совпадает с валидацией на сервере!

from datetime import datetime, timedelta

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from cleanpro.app_data import ORDER_CANCELLED_STATUS
from users.models import Address


class Measure(models.Model):
    """Модель единиц измерения услуг."""

    title = models.CharField(
        verbose_name='Единица измерения',
        max_length=25,
        unique=True,
    )

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'

    def __str__(self):
        return self.title


class Service(models.Model):
    """Модель услуг."""

    SERVICE_TYPE = [
        ('main', 'Основная'),
        ('additional', 'Дополнительная'),
    ]

    title = models.CharField(
        verbose_name='Название услуги',
        max_length=60,
        unique=True
    )
    price = models.FloatField(
        verbose_name='Цена услуги за единицу услуги',
        max_length=7,
        validators=(
            MinValueValidator(1, 'Укажите корректную сумму.'),
        ),
    )
    measure = models.ForeignKey(
        Measure,
        verbose_name='Единица измерения услуги',
        related_name='services',
        on_delete=models.PROTECT,
    )
    image = models.ImageField(
        upload_to='service_photo/',
        verbose_name='Изображение услуги',
        null=True,
        blank=True,
    )
    service_type = models.CharField(
        verbose_name='Тип услуги',
        choices=SERVICE_TYPE,
        max_length=11,
        default='main',
    )
    cleaning_time = models.IntegerField(
        verbose_name='Время на услугу',
        validators=(
            MinValueValidator(1, 'Укажите корректное время!'),
        ),
    )

    class Meta:
        verbose_name = 'Услуга и цена'
        verbose_name_plural = 'Услуги и цены'

    def __str__(self):
        return self.title


class CleaningType(models.Model):
    """Модель наборов услуг."""

    title = models.CharField(
        verbose_name='Название наборов услуг.',
        max_length=25,
        unique=True,
    )
    coefficient = models.FloatField(
        verbose_name='Коэффициент повышения цены',
        max_length=3,
        validators=(
            MinValueValidator(1, 'Коэффициент не может быть меньше 1'),
        ),
    )
    service = models.ManyToManyField(
        Service,
        through='ServicesInCleaningType',
        through_fields=('cleaning_type', 'service',),
    )

    class Meta:
        verbose_name = 'Набор услуг'
        verbose_name_plural = 'Наборы услуг'

    def __str__(self):
        return self.title


class ServicesInCleaningType(models.Model):
    """Модель перечня услуг в наборах услуг."""

    cleaning_type = models.ForeignKey(
        CleaningType,
        related_name='services_in_cleaning',
        on_delete=models.CASCADE,
        verbose_name='Набор услуг',
    )
    service = models.ForeignKey(
        Service,
        related_name='services_in_cleaning',
        on_delete=models.CASCADE,
        verbose_name='Услуга',
    )

    class Meta:
        verbose_name = 'Услуга в наборе'
        verbose_name_plural = 'Услуги в наборе'


class Order(models.Model):
    """Модель заказа."""

    STATUS_CHOICES = (
        ('created', 'Создан'),
        ('accepted', 'Принят'),
        ('finished', 'Завершен'),
        (ORDER_CANCELLED_STATUS, 'Отменен'),
    )
    user = models.ForeignKey(
        verbose_name='Заказчик',
        to=settings.AUTH_USER_MODEL,
        related_name='orders',
        # TODO: изучить вопрос, как бы сохранить историю заказов.
        on_delete=models.SET_NULL,
        null=True,
    )
    cleaner = models.ForeignKey(
        verbose_name='Уборщик',
        to=settings.AUTH_USER_MODEL,
        related_name='work_orders',
        # TODO: изучить вопрос, как бы сохранить клинера.
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    total_sum = models.IntegerField(
        verbose_name='Сумма',
        validators=[
            MinValueValidator(1, 'Укажите корректную итоговую сумму!'),
        ]
    )
    total_time = models.IntegerField(
        verbose_name='Суммарное время',
        validators=(
            MinValueValidator(1, 'Укажите корректное время!'),
        ),
    )
    comment = models.CharField(
        verbose_name='Комментарий',
        max_length=512,
        default=None,
        blank=True,
        null=True,
    )
    comment_cancel = models.CharField(
        verbose_name='Комментарий отмены',
        max_length=512,
        default=None,
        blank=True,
        null=True,
    )
    order_status = models.CharField(
        verbose_name='Статус заказа',
        choices=STATUS_CHOICES,
        default='Создан',
        max_length=512,
    )
    cleaning_type = models.ForeignKey(
        CleaningType,
        verbose_name='Наборы услуг',
        related_name='orders',
        on_delete=models.PROTECT,
    )
    services = models.ManyToManyField(
        Service,
        through='ServicesInOrder',
        through_fields=('order', 'service'),
        verbose_name='Услуги',
    )
    rooms_number = models.IntegerField(
        verbose_name='Количество комнат',
        validators=[
            MinValueValidator(1, 'Укажите корректное значение комнат!'),
        ]
    )
    bathrooms_number = models.IntegerField(
        verbose_name='Количество санузлов',
        validators=[
            MinValueValidator(1, 'Укажите корректное значение санузлов!'),
        ]
    )
    pay_status = models.BooleanField(
        default=False,
        verbose_name='Статус оплаты',
    )
    address = models.ForeignKey(
        verbose_name='Адрес',
        to=Address,
        related_name='orders',
        on_delete=models.CASCADE,
    )
    creation_date = models.DateField(
        verbose_name='Дата создания',
        auto_now_add=True,
    )
    creation_time = models.TimeField(
        verbose_name='Время создания',
        auto_now_add=True,
    )
    cleaning_date = models.DateField(
        verbose_name='Дата уборки',
        db_index=True,
    )
    cleaning_time = models.TimeField(
        verbose_name='Время уборки',
    )
    cleaning_time_end = models.TimeField(
        verbose_name='Время окончания уборки',
        blank=True,
        null=True,
    )
    cancel_date = models.DateField(
        verbose_name='Дата отмены заказа',
        db_index=True,
        blank=True,
        null=True,
    )
    cancel_time = models.TimeField(
        verbose_name='Время отмены заказа',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ('-cleaning_date',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"Заказ №: {self.id}"

    def save(self, *args, **kwargs):
        time_start: datetime = datetime.combine(
            date=self.cleaning_date,
            time=self.cleaning_time,
        )
        time_end = time_start + timedelta(minutes=self.total_time)
        self.cleaning_time_end = time_end.time()
        super(Order, self).save(*args, **kwargs)


class ServicesInOrder(models.Model):
    """Модель перечня услуг в заказе."""

    order = models.ForeignKey(
        Order,
        related_name='services_in_order',
        on_delete=models.CASCADE,
        verbose_name='Заказ',
    )
    service = models.ForeignKey(
        Service,
        related_name='services_in_order',
        on_delete=models.CASCADE,
        verbose_name='Услуга',
    )
    amount = models.PositiveIntegerField(
        validators=(
            MinValueValidator(
                0, 'Укажите корректное значение количества услуг.'
            ),
        ),
        verbose_name='Количество',
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Услуги в заказе'
        verbose_name_plural = 'Услуги в заказах'


class Rating(models.Model):
    """Модель отзывов заказов

    Включает в себя как отзывы по заказам, так и отзывы с Я.Карт.

    При сохранении отзывов с Я.Карт поля user и order не заполняются.
    При сохранении отзывов по заказам также заполняется поле username.

    Поле username используется для отображении отзыва на главной странице
    сайта."""

    username = models.CharField(
        verbose_name='Отображаемое имя заказчика',
        max_length=60,
        blank=True,
    )
    user = models.ForeignKey(
        verbose_name='Заказчик',
        to=settings.AUTH_USER_MODEL,
        related_name='ratings',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    from_maps = models.BooleanField(
        verbose_name='Отзыв с Я.Карт',
        default=False,
    )
    order = models.ForeignKey(
        verbose_name='Заказа',
        to=Order,
        related_name='rating',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата отзыва',
        auto_now_add=True,
        db_index=True,
    )
    text = models.CharField(
        verbose_name='Текст отзыва',
        max_length=512,
    )
    score = models.IntegerField(
        verbose_name='Оценка',
        validators=(
            MinValueValidator(1, 'Укажите оценку от 1 до 5.'),
            MaxValueValidator(5, 'Укажите оценку от 1 до 5.'),
        ),
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=('user', 'order'),
            name='unique_user_order_rating'
        )]
        ordering = ('-id',)
        verbose_name = 'Отзыв заказа'
        verbose_name_plural = 'Отзывы заказов'

    def save(self, *args, **kwargs):
        """
        Добавляет значение поля username для пользователей,
        которые оставили отзыв на сайте к заказу.
        """
        if self.user:
            self.username = self.user.username
        super().save(*args, **kwargs)
        return

    def __str__(self):
        return (
            f'Отзыв {self.username} с оценкой {self.score} от {self.pub_date}.'
        )
