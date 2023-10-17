from django.contrib import admin

from cleanpro.app_data import ADMIN_LIST_PER_PAGE
from services.models import (
    CleaningType, Measure, Order, Rating, Service,
    ServicesInCleaningType, ServicesInOrder
)
from users.models import User


class ServicesInCleaningTypeInline(admin.StackedInline):
    """
    Инлайн для отображения записей модели ServicesInCleaningType в стековой
    форме с вертикальными блоками редактирования.

    Атрибуты:
        - модель ServicesInCleaningType (model)
        - количество дополнительных пустых форм (extra)
    """
    model = ServicesInCleaningType
    extra = 1


@admin.register(CleaningType)
class CleaningTypeAdmin(admin.ModelAdmin):
    """
    Переопределяет административный интерфейс Django для модели CleaningType.

    Атрибуты:
        - list_display (tuple) - список полей для отображения в интерфейсе:
            - ID набора услуг (pk)
            - название набора услуг (title)
            - коэффициент повышения цены (coefficient)
            - сервисы набора услуг (через метод services_list)
        - inlines (tuple): определяет отображение связанных моделей:
            - отображает сервисы в наборе услуг (ServicesInCleaningTypeInline)
        - list_editable (tuple) - список полей для изменения в интерфейсе:
            - название набора услуг (title)
            - коэффициент повышения цены (coefficient)
        - list_filter (tuple) - список фильтров:
            - коэффициент повышения цены (coefficient)
        - search_fields (tuple) - список полей для поиска объектов:
            - название набора услуг (title)
        - list_per_page (int) - количество объектов на одной странице

    Методы:
        - services_list - возвращает строковое перечисление всех сервисов и их
                          количества в заказе для показа в list_display.
                          Атрибут short_description устанавливает название
                          столбца в интерфейсе
    """
    list_display = (
        'pk',
        'title',
        'coefficient',
        'services_list',
    )
    list_editable = (
        'title',
        'coefficient',
    )
    list_filter = (
        'coefficient',
    )
    search_fields = (
        'title',
    )
    list_per_page = ADMIN_LIST_PER_PAGE
    inlines = (ServicesInCleaningTypeInline,)

    @admin.display(description='services')
    def services_list(self, obj):
        return [p.title for p in obj.service.all()]

    services_list.short_description = 'Список сервисов'


@admin.register(Measure)
class MeasureAdmin(admin.ModelAdmin):
    """
    Переопределяет административный интерфейс Django для модели Measure.

    Атрибуты:
        - list_display (tuple) - список полей для отображения в интерфейсе:
            - ID набора услуг (pk)
            - название единицы измерения (title)
        - list_editable (tuple) - список полей для изменения в интерфейсе:
            - название единицы измерения (title)
        - search_fields (tuple) - список полей для поиска объектов:
            - название единицы измерения (title)
        - list_per_page (int) - количество объектов на одной странице
    """
    list_display = (
        'pk',
        'title',
    )
    list_editable = (
        'title',
    )
    search_fields = (
        'title',
    )
    list_per_page = ADMIN_LIST_PER_PAGE


class ServicesInOrderInline(admin.StackedInline):
    """
    Инлайн для отображения записей модели ServicesInOrder в стековой
    форме с вертикальными блоками редактирования.

    Атрибуты:
        - модель ServicesInOrder (model)
        - количество дополнительных пустых форм (extra)
    """
    model = ServicesInOrder
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    """
    Переопределяет ModelAdmin для модели Order:
        - в поле уборщик (cleaner) выводит только пользователей,
          которые имеют статус is_cleaner=True
    """

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'cleaner':
            kwargs['queryset'] = User.objects.filter(is_cleaner=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Order)
class OrderAdmin(OrderAdmin):
    """
    Переопределяет административный интерфейс Django для модели Order.

    Атрибуты:
        - list_display (tuple) - список полей для отображения в интерфейсе:
            - ID заказа (pk)
            - ID заказчика (user)
            - ID уборщика (cleaner)
            - статус заказа (order_status)
            - статус оплаты (pay_status)
            - суммарное время работ (total_time)
            - сумма заказа (total_sum)
            - ID адреса (address)
            - комментарий заказа (comment)
            - тип уборки (cleaning_type)
            - список сервисов и их количество в заказе (services_list)
            - количество комнат (rooms_number)
            - количество санузлов (bathrooms_number)
            - дата создания заказа (creation_date)
            - время создания заказа (creation_time)
            - дата начала уборки (cleaning_date)
            - время начала уборки (cleaning_time)
            - время окончания уборки (cleaning_time_end)
            - комментарий отмены заказа (comment_cancel)
            - дата отмены заказа (cancel_date)
            - время отмены заказа (cancel_time)
        - inlines (tuple): определяет отображение связанных моделей:
            - отображает сервисы в заказе (ServicesInOrderInline)
        - list_editable (tuple) - список полей для изменения в интерфейсе:
            - ID уборщика (cleaner)
            - статус заказа (order_status)
            - статус оплаты (pay_status)
            - сумма заказа (total_sum)
            - комментарий заказа (comment)
            - комментарий отмены заказа (comment_cancel)
            - дата начала уборки (cleaning_date)
            - время начала уборки (cleaning_time)
        - list_filter (tuple) - список фильтров:
            - статус заказа (order_status)
        - search_fields (tuple) - список полей для поиска объектов:
            - ID заказчика (user)
        - list_per_page (int) - количество объектов на одной странице

    Методы:
        - services_list - возвращает строковое перечисление всех сервисов и их
                          количества в заказе для показа в list_display.
                          Атрибут short_description устанавливает название
                          столбца в интерфейсе
    """
    list_display = (
        'pk',
        'user',
        'cleaner',
        'order_status',
        'pay_status',
        'total_time',
        'total_sum',
        'address',
        'comment',
        'cleaning_type',
        'services_list',
        'rooms_number',
        'bathrooms_number',
        'creation_date',
        'creation_time',
        'cleaning_date',
        'cleaning_time',
        'cleaning_time_end',
        'comment_cancel',
        'cancel_date',
        'cancel_time',
    )
    inlines = (ServicesInOrderInline,)
    list_editable = (
        'cleaner',
        'order_status',
        'pay_status',
        'total_sum',
        'comment',
        'comment_cancel',
        'cleaning_date',
        'cleaning_time',
    )
    list_filter = ('order_status',)
    search_fields = ('user',)
    list_per_page = ADMIN_LIST_PER_PAGE

    def services_list(self, obj):
        services = [
            f'{service} ({service.services_in_order.get(order=obj).amount})'
            for service in obj.services.all()
        ]
        return ',\n'.join(services)

    services_list.short_description = 'Список сервисов'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """
    Переопределяет административный интерфейс Django для модели Rating.

    Атрибуты:
        - list_display (tuple) - список полей для отображения в интерфейсе:
            - ID отзыва (pk)
            - отображаемое имя заказчика (username)
            - ID заказчика (user)
            - получен ли отзыв с Я.Карт (from_maps)
            - ID заказа (order)
            - дата публикации (pub_date)
            - текст отзыва (text)
            - оценка заказа (score)
        - list_editable (tuple) - список полей для изменения в интерфейсе:
            - текст отзыва (text)
            - оценка заказа (score)
        - list_filter (tuple) - список фильтров:
            - оценка заказа (score)
        - search_fields (tuple) - список полей для поиска объектов:
            - ID заказчика (user)
        - list_per_page (int) - количество объектов на одной странице
    """
    list_display = (
        'pk',
        'username',
        'user',
        'from_maps',
        'order',
        'pub_date',
        'text',
        'score',
    )
    list_editable = (
        'username',
        'text',
        'score',
    )
    list_filter = (
        'from_maps',
        'score',
    )
    search_fields = (
        'username',
        'user',
    )
    list_per_page = ADMIN_LIST_PER_PAGE


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """
    Переопределяет административный интерфейс Django для модели Service.

    Атрибуты:
        - list_display (tuple) - список полей для отображения в интерфейсе:
            - ID услуги (pk)
            - название услуги (title)
            - цена за единицу услуги (price)
            - единица измерения услуги (measure)
            - изображение услуги (image)
            - тип услуги (service_type)
            - время на услугу (cleaning_time)
        - list_editable (tuple) - список полей для изменения в интерфейсе:
            - название услуги (title)
            - цена за единицу услуги (price)
            - единица измерения услуги (measure)
            - изображение услуги (image)
            - тип услуги (service_type)
            - время на услугу (cleaning_time)
        - list_filter (tuple) - список фильтров:
            - цена за единицу услуги (price)
            - единица измерения услуги (measure)
            - тип услуги (service_type)
            - время на услугу (cleaning_time)
        - search_fields (tuple) - список полей для поиска объектов:
            - название услуги (title)
        - list_per_page (int) - количество объектов на одной странице
    """
    list_display = (
        'pk',
        'title',
        'price',
        'measure',
        'image',
        'service_type',
        'cleaning_time',
    )
    list_editable = (
        'title',
        'price',
        'measure',
        'image',
        'service_type',
        'cleaning_time',
    )
    list_filter = (
        'price',
        'measure',
        'service_type',
        'cleaning_time',
    )
    search_fields = (
        'title',
    )
    list_per_page = ADMIN_LIST_PER_PAGE
