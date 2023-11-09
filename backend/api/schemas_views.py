from rest_framework import status, serializers
from drf_spectacular.utils import inline_serializer, extend_schema

from api.serializers import (
    AdminOrderPatchSerializer,
    CleaningGetTimeSerializer,
    CreateCleaningTypeSerializer,
    CreateServiceSerializer,
    GetCleaningTypeSerializer,
    GetServiceSerializer,
    MeasureSerializer,
    OrderGetSerializer,
    OrderPostSerializer,
    OrderRatingSerializer,
    RatingSerializer,
    UserRegisterSerializer,
    UserSerializer,
)

DEFAULT_400: str = 'Невозможно войти с предоставленными учетными данными.'
DEFAULT_401: str = 'Недопустимый токен.'
DEFAULT_403: str = 'У вас недостаточно прав для выполнения данного действия.'
DEFAULT_404: str = 'Страница не найдена.'
DEFAULT_REQUIRED: str = 'Обязательное поле.'


CLEANING_TYPES_SCHEMA = {
    'list': extend_schema(
        description='Возвращает список типов уборки.',
        summary='Получить список типов уборки.',
        responses={
            status.HTTP_200_OK: GetCleaningTypeSerializer,
        },
    ),
    'create': extend_schema(
        description='Создает новый тип уборки.',
        summary='Создать новый тип уборки.',
        responses={
            status.HTTP_201_CREATED: CreateCleaningTypeSerializer,
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                name='cleaning_types_create_error_400',
                fields={
                    'title': serializers.ListField(
                        default=[DEFAULT_REQUIRED],
                    ),
                    'coefficient': serializers.ListField(
                        default=[DEFAULT_REQUIRED],
                    ),
                    'service': serializers.ListField(
                        default=[DEFAULT_REQUIRED],
                    ),
                },
            ),
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='cleaning_types_create_error_401',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_401)
                },
            ),
            status.HTTP_403_FORBIDDEN: inline_serializer(
                name='cleaning_types_create_error_403',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_403)
                },
            ),
        },
    ),
    'retrieve': extend_schema(
        description='Возвращает тип уборки с указанным идентификатором.',
        summary='Получить тип уборки.',
        responses={
            status.HTTP_200_OK: GetCleaningTypeSerializer,
            status.HTTP_404_NOT_FOUND: inline_serializer(
                name='cleaning_types_retrieve_error_404',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_404)
                },
            ),
        },
    ),
    'update': extend_schema(
        description='Обновляет тип уборки с указанным идентификатором.',
        summary='Обновить тип уборки.',
        responses={
            status.HTTP_200_OK: GetCleaningTypeSerializer,
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                name='cleaning_types_update_error_400',
                fields={
                    'detail': serializers.CharField(default='string')
                },
            ),
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='cleaning_types_update_error_401',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_401)
                },
            ),
            status.HTTP_403_FORBIDDEN: inline_serializer(
                name='cleaning_types_update_error_403',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_403)
                },
            ),
            status.HTTP_404_NOT_FOUND: inline_serializer(
                name='cleaning_types_update_error_404',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_404)
                },
            ),
        },
    ),
}

MEASURE_SCHEMA = {
    'list': extend_schema(
        description='Возвращает список единиц измерения.',
        summary='Получить список единиц измерений.',
        responses={
            status.HTTP_200_OK: MeasureSerializer,
        },
    ),
    'create': extend_schema(
        description='Создает новую единиц измерения.',
        summary='Создать новую единицу измерения.',
        responses={
            status.HTTP_201_CREATED: MeasureSerializer,
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                name='measures_create_error_400',
                fields={
                    'title': serializers.ListField(
                        default=[DEFAULT_REQUIRED],
                    ),
                },
            ),
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='measures_create_error_401',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_401)
                },
            ),
            status.HTTP_403_FORBIDDEN: inline_serializer(
                name='measures_create_error_403',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_403)
                },
            ),
        },
    ),
    'retrieve': extend_schema(
        description=(
            'Возвращает единицу измерения с указанным идентификатором.'
        ),
        summary='Получить единицу измерения.',
        responses={
            status.HTTP_200_OK: MeasureSerializer,
            status.HTTP_404_NOT_FOUND: inline_serializer(
                name='measures_retrieve_error_404',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_404)
                },
            ),
        },
    ),
    'update': extend_schema(
        description='Обновляет единицу измерения с указанным идентификатором.',
        summary='Обновить единицу измерения.',
        responses={
            status.HTTP_200_OK: MeasureSerializer,
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                name='measures_update_error_400',
                fields={
                    'title': serializers.ListField(
                        default=[DEFAULT_REQUIRED],
                    ),
                },
            ),
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='measures_update_error_401',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_401)
                },
            ),
            status.HTTP_403_FORBIDDEN: inline_serializer(
                name='measures_update_error_403',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_403)
                },
            ),
            status.HTTP_404_NOT_FOUND: inline_serializer(
                name='measures_update_error_404',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_404)
                },
            ),
        },
    ),
    'destroy': extend_schema(
        description='Удаляет единицу измерения с указанным идентификатором.',
        summary='Удалить единицу измерения.',
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='measures_destroy_error_401',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_401)
                },
            ),
            status.HTTP_403_FORBIDDEN: inline_serializer(
                name='measures_destroy_error_403',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_403)
                },
            ),
            status.HTTP_404_NOT_FOUND: inline_serializer(
                name='measures_destroy_error_404',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_404)
                },
            ),
        },
    ),
}

ORDER_SCHEMA = {
    'list': extend_schema(
        description='Возвращает список заказов.',
        summary='Получить список заказов.',
        responses={
            status.HTTP_200_OK: OrderGetSerializer,
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='orders_list_error_401',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_401)
                },
            ),
        },
    ),
    'create': extend_schema(
        description='Создает новый заказ.',
        summary='Создать новый заказ.',
        request=OrderPostSerializer,
        responses={
            status.HTTP_201_CREATED: inline_serializer(
                name='orders_create_201',
                fields={
                    'Статус': serializers.CharField(default='Заказ создан.')
                },
            ),
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                name='orders_create_error_400',
                fields={
                    'user': serializers.ListField(
                        default=[DEFAULT_REQUIRED],
                    ),
                    'total_sum': serializers.ListField(
                        default=[DEFAULT_REQUIRED],
                    ),
                    'total_time': serializers.ListField(
                        default=[DEFAULT_REQUIRED],
                    ),
                    'cleaning_type': serializers.ListField(
                        default=[DEFAULT_REQUIRED],
                    ),
                    'services': serializers.ListField(
                        default=[DEFAULT_REQUIRED],
                    ),
                    'rooms_number': serializers.ListField(
                        default=[DEFAULT_REQUIRED],
                    ),
                    'bathrooms_number': serializers.ListField(
                        default=[DEFAULT_REQUIRED],
                    ),
                    'address': serializers.ListField(
                        default=[DEFAULT_REQUIRED],
                    ),
                    'cleaning_date': serializers.ListField(
                        default=[DEFAULT_REQUIRED],
                    ),
                    'cleaning_time': serializers.ListField(
                        default=[DEFAULT_REQUIRED],
                    ),
                },
            ),
        },
    ),
    'retrieve': extend_schema(
        description='Возвращает заказ с указанным идентификатором.',
        summary='Получить заказ.',
        responses={
            status.HTTP_200_OK: OrderGetSerializer,
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='orders_retrieve_error_401',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_401)
                },
            ),
            status.HTTP_404_NOT_FOUND: inline_serializer(
                name='orders_retrieve_error_404',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_404)
                },
            ),
        },
    ),
    'update': extend_schema(
        description='Обновляет заказ с указанным идентификатором.',
        summary='Обновить заказ.',
        responses={
            status.HTTP_200_OK: AdminOrderPatchSerializer,
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                name='orders_update_error_400',
                fields={
                    'order_status': serializers.ListField(
                        default=[
                            'Вы можете установить только статус отмены заказа.'
                        ],
                    )
                },
            ),
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='orders_update_error_401',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_401)
                },
            ),
            status.HTTP_404_NOT_FOUND: inline_serializer(
                name='orders_update_error_404',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_404)
                },
            ),
        },
    ),
    'pay': extend_schema(
        description=(
            'Устанавливает статус заказа с '
            'указанным идентификатором как "оплачено".'
        ),
        summary='Оплатить заказ.',
        request=None,
        responses={
            status.HTTP_200_OK: inline_serializer(
                name='orders_pay_200',
                fields={
                    'pay_status': serializers.BooleanField(default=True)
                },
            ),
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='orders_pay_error_401',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_401)
                },
            ),
            status.HTTP_403_FORBIDDEN: inline_serializer(
                name='orders_pay_error_403',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_403)
                },
            ),
            status.HTTP_404_NOT_FOUND: inline_serializer(
                name='orders_pay_error_404',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_404)
                },
            ),
        }
    ),
    'rating': extend_schema(
        description=(
            'Создает отзыв к заказу с указанным идентификатором.'
        ),
        summary='Создать отзыв к заказу.',
        request=OrderRatingSerializer,
        responses={
            status.HTTP_200_OK: OrderRatingSerializer,
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                name='orders_ratings_error_400',
                fields={
                    'order_status': serializers.ListField(
                        default=[
                            'Оставить отзыв на незавершенный заказ невозможно.'
                        ],
                    ),
                    'rating_exists': serializers.ListField(
                        default=[
                            'Отзыв на этот заказ уже существует.'
                        ],
                    ),
                    'cleaning_date': serializers.ListField(
                        default=[DEFAULT_REQUIRED],
                    ),
                    'total_time': serializers.ListField(
                        default=[DEFAULT_REQUIRED],
                    ),
                },
            ),
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='orders_ratings_error_401',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_401)
                },
            ),
            status.HTTP_404_NOT_FOUND: inline_serializer(
                name='orders_ratings_error_404',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_404)
                },
            ),
        },
    ),
    'get_available_time': extend_schema(
        description=(
            'Получает доступное время для за дату к заказу '
            'с указанным идентификатором.'
        ),
        summary='Получить доступную дату и время для заказа.',
        request=CleaningGetTimeSerializer,
        responses={
            status.HTTP_200_OK: inline_serializer(
                name='orders_get_available_time_200',
                fields={
                    '00:00': serializers.BooleanField(default=False),
                    '00:30': serializers.BooleanField(default=False),
                    '01:00': serializers.BooleanField(default=False),
                    '01:30': serializers.BooleanField(default=False),
                    '02:00': serializers.BooleanField(default=False),
                    '02:30': serializers.BooleanField(default=False),
                    '03:00': serializers.BooleanField(default=False),
                    '03:30': serializers.BooleanField(default=False),
                    '04:00': serializers.BooleanField(default=False),
                    '04:30': serializers.BooleanField(default=False),
                    '05:00': serializers.BooleanField(default=False),
                    '05:30': serializers.BooleanField(default=False),
                    '06:00': serializers.BooleanField(default=False),
                    '06:30': serializers.BooleanField(default=False),
                    '07:00': serializers.BooleanField(default=False),
                    '07:30': serializers.BooleanField(default=False),
                    '08:00': serializers.BooleanField(default=False),
                    '08:30': serializers.BooleanField(default=False),
                    '09:00': serializers.BooleanField(default=True),
                    '09:30': serializers.BooleanField(default=True),
                    '10:00': serializers.BooleanField(default=True),
                    '10:30': serializers.BooleanField(default=True),
                    '11:00': serializers.BooleanField(default=True),
                    '11:30': serializers.BooleanField(default=True),
                    '12:00': serializers.BooleanField(default=True),
                    '12:30': serializers.BooleanField(default=True),
                    '13:00': serializers.BooleanField(default=True),
                    '13:30': serializers.BooleanField(default=True),
                    '14:00': serializers.BooleanField(default=True),
                    '14:30': serializers.BooleanField(default=True),
                    '15:00': serializers.BooleanField(default=True),
                    '15:30': serializers.BooleanField(default=True),
                    '16:00': serializers.BooleanField(default=True),
                    '16:30': serializers.BooleanField(default=True),
                    '17:00': serializers.BooleanField(default=True),
                    '17:30': serializers.BooleanField(default=True),
                    '18:00': serializers.BooleanField(default=True),
                    '18:30': serializers.BooleanField(default=True),
                    '19:00': serializers.BooleanField(default=False),
                    '19:30': serializers.BooleanField(default=False),
                    '20:00': serializers.BooleanField(default=False),
                    '20:30': serializers.BooleanField(default=False),
                    '21:00': serializers.BooleanField(default=False),
                    '21:30': serializers.BooleanField(default=False),
                    '22:00': serializers.BooleanField(default=False),
                    '22:30': serializers.BooleanField(default=False),
                    '23:00': serializers.BooleanField(default=False),
                    '23:30': serializers.BooleanField(default=False),
                },
            ),
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                name='orders_get_available_time_error_400',
                fields={
                    'cleaning_date': serializers.ListField(
                        default=[DEFAULT_REQUIRED],
                    ),
                    'total_time': serializers.ListField(
                        default=[DEFAULT_REQUIRED],
                    ),
                },
            ),
        },
    ),
}

RATING_SCHEMA = {
    'list': extend_schema(
        description='Возвращает список отзывов.',
        summary='Получить список отзывов.',
        responses={
            status.HTTP_200_OK: RatingSerializer,
        },
    ),
    'retrieve': extend_schema(
        description='Возвращает отзыв с указанным идентификатором.',
        summary='Получить отзыв.',
        responses={
            status.HTTP_200_OK: RatingSerializer,
            status.HTTP_404_NOT_FOUND: inline_serializer(
                name='rating_retrieve_error_404',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_404)
                },
            ),
        },
    ),
    'partial_update': extend_schema(
        description='Обновляет отзыв с указанным идентификатором.',
        summary='Обновить существующий отзыв.',
        responses={
            status.HTTP_200_OK: RatingSerializer,
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                name='ratings_update_error_400',
                fields={
                    'detail': serializers.CharField(default='string')
                },
            ),
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='ratings_update_error_401',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_401)
                },
            ),
            status.HTTP_404_NOT_FOUND: inline_serializer(
                name='ratings_update_error_404',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_404)
                },
            ),
        },
    ),
}

SERVICE_SCHEMA = {
    'list': extend_schema(
        description='Возвращает список услуг.',
        summary='Получить список услуг.',
        responses={
            status.HTTP_200_OK: GetServiceSerializer,
        },
    ),
    'create': extend_schema(
        description='Создает новый услугу.',
        summary='Создать новую услугу.',
        responses={
            status.HTTP_201_CREATED: CreateServiceSerializer,
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                name='services_create_error_400',
                fields={
                    'title': serializers.ListField(
                        default=[DEFAULT_REQUIRED],
                    ),
                    'price': serializers.ListField(
                        default=[DEFAULT_REQUIRED],
                    ),
                    'measure': serializers.ListField(
                        default=[DEFAULT_REQUIRED],
                    ),
                    'image': serializers.ListField(
                        default=['Ни одного файла не было отправлено.'],
                    ),
                    'cleaning_time': serializers.ListField(
                        default=[DEFAULT_REQUIRED],
                    ),
                },
            ),
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='services_create_error_401',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_401)
                },
            ),
            status.HTTP_403_FORBIDDEN: inline_serializer(
                name='services_create_error_403',
                fields={
                    'detail': serializers.CharField(default=(DEFAULT_403)),
                },
            ),
        },
    ),
    'retrieve': extend_schema(
        description='Возвращает услугу с указанным идентификатором.',
        summary='Получить услугу.',
        responses={
            status.HTTP_200_OK: GetServiceSerializer,
            status.HTTP_404_NOT_FOUND: inline_serializer(
                name='services_retrieve_error_404',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_404)
                },
            ),
        },
    ),
    'update': extend_schema(
        description='Обновляет услугу с указанным идентификатором.',
        summary='Обновить существующую услугу.',
        responses={
            status.HTTP_200_OK: GetServiceSerializer,
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='services_update_error_401',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_401)
                },
            ),
            status.HTTP_403_FORBIDDEN: inline_serializer(
                name='services_update_error_403',
                fields={
                    'detail': serializers.CharField(default=(DEFAULT_403)),
                },
            ),
            status.HTTP_404_NOT_FOUND: inline_serializer(
                name='services_update_error_404',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_404)
                },
            ),
        },
    ),
}

TOKEN_CREATE_SCHEMA = {
    'description': 'Создает токен авторизации.',
    'summary': 'Создать токен авторизации.',
    'responses': {
        status.HTTP_200_OK: inline_serializer(
            name='login_200',
            fields={'auth_token': serializers.CharField(default='string')},
        ),
        status.HTTP_400_BAD_REQUEST: inline_serializer(
            name='login_400',
            fields={
                'non_field_errors': serializers.ListField(
                    default=[DEFAULT_400],
                )
            },
        ),
    },
}

TOKEN_DESTROY_SCHEMA = {
    'description': 'Удаляет токен авторизации.',
    'summary': 'Удалить токен авторизации.',
    'responses': {
        status.HTTP_204_NO_CONTENT: None,
        status.HTTP_401_UNAUTHORIZED: inline_serializer(
            name='logout_401',
            fields={
                'detail': serializers.CharField(
                    default=DEFAULT_401,
                ),
            },
        ),
    },
}

USER_SCHEMA = {
    'list': extend_schema(
        description='Возвращает список пользователей.',
        summary='Получить список пользователей.',
        responses={
            status.HTTP_200_OK: UserSerializer,
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='users_list_error_401',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_401)
                },
            ),
            status.HTTP_403_FORBIDDEN: inline_serializer(
                name='users_list_error_403',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_403)
                },
            ),
        },
    ),
    'create': extend_schema(
        description='Создает нового пользователя.',
        summary='Создать нового пользователя.',
        responses={
            status.HTTP_201_CREATED: UserRegisterSerializer,
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                name='users_create_error_400',
                fields={
                    'email': serializers.CharField(
                        default=(
                            'Пользователь с таким адресом электронной '
                            'почты уже зарегистрирован.'
                        ),
                    ),
                },
            ),
        },
    ),
    'retrieve': extend_schema(
        description=(
            'Возвращает данные пользователя с указанным идентификатором.'
        ),
        summary='Получить данные пользователя.',
        responses={
            status.HTTP_200_OK: UserSerializer,
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='users_retrieve_error_401',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_401)
                },
            ),
            status.HTTP_403_FORBIDDEN: inline_serializer(
                name='users_retrieve_error_403',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_403)
                },
            ),
            status.HTTP_404_NOT_FOUND: inline_serializer(
                name='users_retrieve_error_404',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_404)
                },
            ),
        },
    ),
    'update': extend_schema(
        description=(
            'Обновляет данные пользователя с указанным идентификатором.'
        ),
        summary='Обновить данные пользователя.',
        responses={
            status.HTTP_200_OK: UserSerializer,
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                name='users_update_error_400',
                fields={
                    'detail': serializers.CharField(default='string')
                },
            ),
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='users_update_error_401',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_401)
                },
            ),
            status.HTTP_403_FORBIDDEN: inline_serializer(
                name='users_update_error_403',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_403)
                },
            ),
            status.HTTP_404_NOT_FOUND: inline_serializer(
                name='users_update_error_404',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_404)
                },
            ),
        },
    ),
    'orders': extend_schema(
        description=(
            'Возвращает список заказов пользователя '
            'с указанным идентификатором.'
        ),
        summary='Получить список заказов пользователя.',
        responses={
            status.HTTP_200_OK: OrderGetSerializer,
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='users_orders_list_error_401',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_401)
                },
            ),
            status.HTTP_403_FORBIDDEN: inline_serializer(
                name='users_orders_list_error_403',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_403)
                },
            ),
            status.HTTP_404_NOT_FOUND: inline_serializer(
                name='users_orders_list_error_404',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_404)
                },
            ),
        },
    ),
    'confirm_email': extend_schema(
        summary='Подтверждение электронной почты.',
        description='Подтвердить электронную почту.',
        responses={
            status.HTTP_200_OK: inline_serializer(
                name='users_confirm_email_200',
                fields={
                    'created': serializers.CharField(
                        default=(
                            'Введите пароль вашей учетной записи, который '
                            'был выслан на указанную почту:'
                        ),
                    ),
                },
            ),
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                name='users_confirm_email_error_401',
                fields={
                    'email': serializers.ListField(
                        default=['Введите правильный адрес электронной почты.'],  # noqa (E501)
                    ),
                },
            ),
        },
    ),
    'confirm_password': extend_schema(
        summary='Подтверждение пароля учетной записи.',
        description='Подтвердить пароль учетной записи.',
        responses={
            status.HTTP_200_OK: inline_serializer(
                name='users_confirm_password_200',
                fields={
                    'password': serializers.CharField(
                        default='Пароль успешно подтвержден.'
                    ),
                },
            ),
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                name='users_confirm_password_error_400',
                fields={
                    'password': serializers.CharField(
                        default='Указан неверный пароль.'
                    ),
                },
            ),
        },
    ),
    'me': extend_schema(
        description='Возвращает данные авторизированного пользователя.',
        summary='Получить данные авторизированного пользователя.',
        responses={
            status.HTTP_200_OK: UserSerializer,
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='users_me_error_401',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_401)
                },
            ),
        },
    ),
}
