from django.contrib import admin

from cleanpro.app_data import ADMIN_LIST_PER_PAGE
from users.models import Address, User


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """
    Переопределяет административный интерфейс Django для модели Address.

    Атрибуты:
        - list_display (tuple) - список полей для отображения в интерфейсе:
            - ID адреса (pk)
            - наименование города (city)
            - наименование улицы (street)
            - номер дома (house)
            - номер парадной (entrance)
            - номер этажа (floor)
            - номер квартиры (apartment)
        - list_editable (tuple) - список полей для изменения в интерфейсе:
            - наименование города (city)
            - наименование улицы (street)
            - номер дома (house)
            - номер парадной (entrance)
            - номер этажа (floor)
            - номер квартиры (apartment)
        - list_filter (tuple) - список фильтров:
            - наименование города (city)
            - наименование улицы (street)
        - search_fields (tuple) - список полей для поиска объектов:
            - наименование города (city)
            - наименование улицы (street)
            - номер дома (house)
            - номер парадной (entrance)
            - номер этажа (floor)
            - номер квартиры (apartment)
        - list_per_page (int) - количество объектов на одной странице

    Методы:
        - services_list - возвращает строковое перечисление всех сервисов и их
                          количества в заказе для показа в list_display.
                          Атрибут short_description устанавливает название
                          столбца в интерфейсе
    """
    list_display = (
        'id',
        'city',
        'street',
        'house',
        'entrance',
        'floor',
        'apartment',
    )
    list_editable = (
        'city',
        'street',
        'house',
        'entrance',
        'floor',
        'apartment',
    )
    list_filter = (
        'city',
        'street',
    )
    search_fields = (
        'city',
        'street',
        'house',
        'entrance',
        'floor',
        'apartment',
    )
    list_per_page = ADMIN_LIST_PER_PAGE


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Переопределяет административный интерфейс Django для модели User.

    Атрибуты:
        - list_display (tuple) - список полей для отображения в интерфейсе:
            - ID пользователя (pk)
            - имя пользователя (username)
            - электронная почта пользователя (email)
            - контактный телефон по стандарту E.164 (phone)
            - ID адреса пользователя (address)
            - статус администратора (is_staff)
            - статус уборщика (is_cleaner)
            - начало отпуска уборщика (on_vacation_from)
            - конец отпуска уборщика (on_vacation_to)
        - list_editable (tuple) - список полей для изменения в интерфейсе:
            - имя пользователя (username)
            - электронная почта пользователя (email)
            - контактный телефон по стандарту E.164 (phone)
            - ID адреса пользователя (address)
            - статус уборщика (is_cleaner)
            - начало отпуска уборщика (on_vacation_from)
            - конец отпуска уборщика (on_vacation_to)
        - list_filter (tuple) - список фильтров:
            - статус администратора (is_staff)
            - статус уборщика (is_cleaner)
        - search_fields (tuple) - список полей для поиска объектов:
            - имя пользователя (username)
            - электронная почта пользователя (email)
            - контактный телефон по стандарту E.164 (phone)
            - ID адреса пользователя (address)
        - list_per_page (int) - количество объектов на одной странице

    Методы:
        - services_list - возвращает строковое перечисление всех сервисов и их
                          количества в заказе для показа в list_display.
                          Атрибут short_description устанавливает название
                          столбца в интерфейсе
    """
    list_display = (
        'id',
        'username',
        'email',
        'phone',
        'address',
        'is_staff',
        'is_cleaner',
        'on_vacation_from',
        'on_vacation_to',
    )
    list_editable = (
        'username',
        'email',
        'phone',
        'address',
        'is_cleaner',
        'on_vacation_from',
        'on_vacation_to',
    )
    list_filter = (
        'is_staff',
        'is_cleaner',
    )
    search_fields = (
        'email',
        'username',
        'phone',
    )
    list_per_page = ADMIN_LIST_PER_PAGE
