from rest_framework import status, serializers
from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiParameter,
    # OpenApiResponse,
    inline_serializer,
)
# from drf_spectacular.types import OpenApiTypes

from api.serializers import (
    # AdminOrderPatchSerializer,
    # CleaningGetTimeSerializer,
    # CreateCleaningTypeSerializer,
    # CreateServiceSerializer,
    EmailConfirmSerializer,
    # GetCleaningTypeSerializer,
    # GetServiceSerializer,
    # MeasureSerializer,
    OrderGetSerializer,
    OrderPostSerializer,
    # OrderRatingSerializer,
    # OwnerOrderPatchSerializer,
    # PaySerializer,
    # RatingSerializer,
    UserCreateSerializer,
    UserGetSerializer,
)

# TODO: "api" схема также требует корректировок.

MEASURE_SCHEMA = {
    'list': extend_schema(
        summary="Получить список всех единиц измерений.",
    ),
    'create': extend_schema(
        summary="Создать новую единицу измерения.",
    ),
    'retrieve': extend_schema(
        summary="Получить существующую единицу измерения.",
    ),
    'update': extend_schema(
        summary="Частично изменить существующую единицу измерения.",
    ),
}

ORDER_SCHEMA = {
    'list': extend_schema(
        summary="Получить список всех заказов.",
    ),
    'create': extend_schema(
        summary="Создать новый заказ.",
        request=OrderPostSerializer,
        responses={
            status.HTTP_200_OK: OrderPostSerializer,
            status.HTTP_201_CREATED: inline_serializer(
                name='create',
                fields={
                    'Статус': serializers.CharField(default="Заказ создан.")
                },
            ),
        },
        examples=[
            OpenApiExample(
                "Пример заказа",
                description="Тестовый пример для заказа.",
                value={
                    "user": {
                        "username": "Вика",
                        "email": "elpastel@email.com",
                        "phone": "+7 777 777 77 77"
                    },
                    "comment": "Que paso, amigo? ;)",
                    "total_sum": 1000000,
                    "total_time": 80,
                    "cleaning_type": "1",
                    "services": [
                        {
                            "id": 1,
                            "amount": 2
                        },
                        {
                            "id": 3,
                            "amount": 1
                        }
                    ],
                    "rooms_number": 1,
                    "bathrooms_number": 3,
                    "address": {
                        "city": 11,
                        "street": 11,
                        "house": 15,
                        "entrance": 15,
                        "floor": 15,
                        "apartment": 15
                    },
                    "cleaning_date": "2023-11-12",
                    "cleaning_time": "12:30"
                },
                status_codes=[str(status.HTTP_200_OK)],
            ),
        ],
    ),
    'retrieve': extend_schema(
        summary="Получить существующий заказ.",
    ),
    'update': extend_schema(
        summary="Частично изменить существующий заказ.",
    ),
    'partial_update': extend_schema(
        summary="Полностью изменить существующий заказ.",
    ),
    'pay': extend_schema(
        summary="Изменить статус оплаты существующего заказа.",
    ),
    'rating': extend_schema(
        summary="Получить существующий отзыв к заказу.",
        description="""
            Так же есть запросы POST, PUT к этому эндпоинту,
            но пока это обновление еще не в develop.
            """,
    ),
    'get_available_time': extend_schema(
        summary="Получить доступную дату и время для заказа.",
    ),
}

RATING_SCHEMA = {
    'list': extend_schema(
        summary="Получить список всех отзывов.",
    ),
    'create': extend_schema(
        summary="Создать новый отзыв.",
        description="""
            Создание простого отзыва, без прикрепления к конкретному заказу.
            """,
    ),
    'retrieve': extend_schema(
        summary="Получить существующий отзыв.",
    ),
    'partial_update': extend_schema(
        summary="Полностью изменить существующий отзыв.",
    ),
    'destroy': extend_schema(
        summary="Удалить существующий отзыв.",
    ),
}

SERVICE_SCHEMA = {
    'list': extend_schema(
        summary="Получить список всех услуг.",
    ),
    'create': extend_schema(
        summary="Создать новую услугу.",
    ),
    'retrieve': extend_schema(
        summary="Получить существующую услугу.",
    ),
    'update': extend_schema(
        summary="Частично изменить существующую услугу.",
    ),
}

# TODO: тут и в документации более корректно будет "Cleaning types".
TYPES_CLEANING_SCHEMA = {
    'list': extend_schema(
        summary="Получить список всех типов уборки.",
    ),
    'create': extend_schema(
        summary="Создать новый тип уборки.",
    ),
    'retrieve': extend_schema(
        summary="Получить существующий тип уборки.",
        description="""
            Возвращает тип уборки и список услуг, которые в нее входят.
            """,
    ),
    'update': extend_schema(
        summary="Частично изменить существующий тип уборки.",
    ),
}

USER_SCHEMA = {
    'list': extend_schema(
        summary="Получить список всех пользователей.",
        responses={
            status.HTTP_200_OK: UserGetSerializer,
        },
    ),
    'create': extend_schema(
        summary="Создать нового пользователя.",
        responses={
            status.HTTP_201_CREATED: UserCreateSerializer,
        },
    ),
    'update': extend_schema(
        summary="Частично изменить существующего пользователя.",
        responses={
            status.HTTP_200_OK: UserGetSerializer,
        },
    ),
    'partial_update': extend_schema(
        summary="Полностью изменить существующего пользователя.",
        responses={
            status.HTTP_200_OK: UserGetSerializer,
        },
    ),
    'orders': extend_schema(
        summary="Получить список всех заказов пользователя.",
        responses={
            status.HTTP_200_OK: OrderGetSerializer,
        },
    ),
    'confirm_email': extend_schema(
        summary="Подтверждение электронной почты.",
        description="""
            Смотрит request.data и проверяет следующие данные:
            - email: адрес электронной почты.

            Если данные являются валидными, генерирует произвольный
            код подтверждения электронной почты. Этот код отправляется
            в JSON клиенту и письмом на указанную электронную почту.
            """,
        responses={
            status.HTTP_200_OK: EmailConfirmSerializer,
        },
    ),
    'me': extend_schema(
        summary="Получить данные авторизованного пользователя.",
        description="""
                Так же возвращает два дополнительных поля:
                    'is_staff',
                    'is_cleaner',

                если эти значения равняются True
            """,
        parameters=[
            OpenApiParameter(name="callsign", required=True, type=str),
        ],
        responses={
            status.HTTP_200_OK: UserGetSerializer,
            status.HTTP_500_INTERNAL_SERVER_ERROR: inline_serializer(
                name='PasscodeResponse',
                fields={
                    'passcode': serializers.CharField(),
                }
            ),
        },
    ),
}
