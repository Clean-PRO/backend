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


class TokenDestroySchema(serializers.Serializer):
    """Вспомогательный сериализатор для TOKEN_DESTROY_SCHEMA."""

    password = serializers.CharField()
    email = serializers.CharField()


CLEANING_TYPES_SCHEMA = {
    'list': extend_schema(
        description='Возвращает список типов уборки.',
        summary='Получить список типов уборки.',
        responses={
            status.HTTP_200_OK: GetCleaningTypeSerializer,
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='types_list_error_401',
                fields={
                    'detail': serializers.CharField(
                        default='Учетные данные не были предоставлены.')
                },
            ),
            status.HTTP_403_FORBIDDEN: inline_serializer(
                name='types_list_error_403',
                fields={
                    'detail': serializers.CharField(
                        default='У вас недостаточно прав'
                        'для выполнения данного действия.')
                },
            ),
        },
    ),
    'create': extend_schema(
        description='Создает новый тип уборки.',
        summary='Создать новый тип уборки.',
        responses={
            status.HTTP_201_CREATED: CreateCleaningTypeSerializer,
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                name='types_create_error_400',
                fields={
                    'detail': serializers.CharField(default='string.')
                },
            ),
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='types_create_error_401',
                fields={
                    'detail': serializers.CharField(
                        default='Учетные данные не были предоставлены.')
                },
            ),
            status.HTTP_403_FORBIDDEN: inline_serializer(
                name='types_create_error_403',
                fields={
                    'detail': serializers.CharField(
                        default='У вас недостаточно прав'
                        'для выполнения данного действия.')
                },
            ),
        },
    ),
    'retrieve': extend_schema(
        description=('Возвращает тип уборки '
                     'с указанным идентификатором.'),
        summary='Получить тип уборки.',
        responses={
            status.HTTP_200_OK: GetCleaningTypeSerializer,
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='types_retrieve_error_401',
                fields={
                    'detail': serializers.CharField(
                        default='Учетные данные не были предоставлены.')
                },
            ),
            status.HTTP_403_FORBIDDEN: inline_serializer(
                name='types_retrieve_error_403',
                fields={
                    'detail': serializers.CharField(
                        default='У вас недостаточно прав'
                        'для выполнения данного действия.')
                },
            ),
            status.HTTP_404_NOT_FOUND: inline_serializer(
                name='types_retrieve_error_404',
                fields={
                    'detail': serializers.CharField(
                        default='Страница не найдена.')
                },
            ),
        },
    ),
    'update': extend_schema(
        description=('Обновляет тип уборки '
                     'с указанным идентификатором.'),
        summary='Обновить тип уборки.',
        responses={
            status.HTTP_200_OK: GetCleaningTypeSerializer,
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                name='types_update_error_400',
                fields={
                    'detail': serializers.CharField(default='string')
                },
            ),
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='types_update_error_401',
                fields={
                    'detail': serializers.CharField(
                        default='Учетные данные не были предоставлены.')
                },
            ),
            status.HTTP_403_FORBIDDEN: inline_serializer(
                name='types_update_error_403',
                fields={
                    'detail': serializers.CharField(
                        default='У вас недостаточно прав'
                        'для выполнения данного действия.')
                },
            ),
            status.HTTP_404_NOT_FOUND: inline_serializer(
                name='types_update_error_404',
                fields={
                    'detail': serializers.CharField(
                        default='Страница не найдена.')
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
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='measure_list_error_401',
                fields={
                    'detail': serializers.CharField(
                        default='Учетные данные не были предоставлены.')
                },
            ),
            status.HTTP_403_FORBIDDEN: inline_serializer(
                name='measure_list_error_403',
                fields={
                    'detail': serializers.CharField(
                        default='У вас недостаточно прав'
                        'для выполнения данного действия.')
                },
            ),
        },
    ),
    'create': extend_schema(
        description='Создает новую единиц измерения.',
        summary='Создать новую единицу измерения.',
        responses={
            status.HTTP_201_CREATED: MeasureSerializer,
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                name='measure_create_error_400',
                fields={
                    'detail': serializers.CharField(default='string.')
                },
            ),
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='measure_create_error_401',
                fields={
                    'detail': serializers.CharField(
                        default='Учетные данные не были предоставлены.')
                },
            ),
            status.HTTP_403_FORBIDDEN: inline_serializer(
                name='measure_create_error_403',
                fields={
                    'detail': serializers.CharField(
                        default='У вас недостаточно прав'
                        'для выполнения данного действия.')
                },
            ),
        },
    ),
    'retrieve': extend_schema(
        description=('Возвращает единицу измерения '
                     'с указанным идентификатором.'),
        summary='Получить единицу измерения.',
        responses={
            status.HTTP_200_OK: MeasureSerializer,
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='measure_retrieve_error_401',
                fields={
                    'detail': serializers.CharField(
                        default='Учетные данные не были предоставлены.')
                },
            ),
            status.HTTP_403_FORBIDDEN: inline_serializer(
                name='measure_retrieve_error_403',
                fields={
                    'detail': serializers.CharField(
                        default='У вас недостаточно прав'
                        'для выполнения данного действия.')
                },
            ),
            status.HTTP_404_NOT_FOUND: inline_serializer(
                name='measure_retrieve_error_404',
                fields={
                    'detail': serializers.CharField(
                        default='Страница не найдена.')
                },
            ),
        },
    ),
    'update': extend_schema(
        description=('Обновляет единицу измерения '
                     'с указанным идентификатором.'),
        summary='Обновить единицу измерения.',
        responses={
            status.HTTP_200_OK: MeasureSerializer,
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                name='measure_update_error_400',
                fields={
                    'detail': serializers.CharField(default='string')
                },
            ),
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='measure_update_error_401',
                fields={
                    'detail': serializers.CharField(
                        default='Учетные данные не были предоставлены.')
                },
            ),
            status.HTTP_403_FORBIDDEN: inline_serializer(
                name='measure_update_error_403',
                fields={
                    'detail': serializers.CharField(
                        default='У вас недостаточно прав'
                        'для выполнения данного действия.')
                },
            ),
            status.HTTP_404_NOT_FOUND: inline_serializer(
                name='measure_update_error_404',
                fields={
                    'detail': serializers.CharField(
                        default='Страница не найдена.')
                },
            ),
        },
    ),
    'destroy': extend_schema(
        description=('Удаляет единицу измерения '
                     'с указанным идентификатором.'),
        summary='Удалить единицу измерения.',
        responses={
            status.HTTP_204_NO_CONTENT: inline_serializer(
                name='measure_destroy_202',
                fields={
                    'detail': serializers.CharField(
                        default='Успешно удаленно.')
                },
            ),
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='measure_destroy_error_401',
                fields={
                    'detail': serializers.CharField(
                        default='Учетные данные не были предоставлены.')
                },
            ),
            status.HTTP_403_FORBIDDEN: inline_serializer(
                name='measure_destroy_error_403',
                fields={
                    'detail': serializers.CharField(
                        default='У вас недостаточно прав'
                        'для выполнения данного действия.')
                },
            ),
            status.HTTP_404_NOT_FOUND: inline_serializer(
                name='measure_destroy_error_404',
                fields={
                    'detail': serializers.CharField(
                        default='Страница не найдена.')
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
                name='order_list_error_401',
                fields={
                    'detail': serializers.CharField(
                        default='Учетные данные не были предоставлены.')
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
                name='order_create_201',
                fields={
                    'Статус': serializers.CharField(default='Заказ создан.')
                },
            ),
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                name='order_create_error_400',
                fields={
                    'staring': serializers.CharField(default='string')
                },
            ),
        },
    ),
    'retrieve': extend_schema(
        description=('Возвращает заказ '
                     'с указанным идентификатором.'),
        summary='Получить заказ.',
        responses={
            status.HTTP_200_OK: OrderGetSerializer,
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='order_retrieve_error_401',
                fields={
                    'detail': serializers.CharField(
                        default='Учетные данные не были предоставлены.')
                },
            ),
            status.HTTP_404_NOT_FOUND: inline_serializer(
                name='order_retrieve_error_404',
                fields={
                    'detail': serializers.CharField(
                        default='Страница не найдена.')
                },
            ),
        },
    ),
    'update': extend_schema(
        description=('Обновляет заказ '
                     'с указанным идентификатором.'),
        summary='Обновить заказ.',
        responses={
            status.HTTP_200_OK: AdminOrderPatchSerializer,
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                name='order_update_error_400',
                fields={
                    'detail': serializers.CharField(default='string')
                },
            ),
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='order_update_error_401',
                fields={
                    'detail': serializers.CharField(
                        default='Учетные данные не были предоставлены.')
                },
            ),
            status.HTTP_404_NOT_FOUND: inline_serializer(
                name='order_update_error_404',
                fields={
                    'detail': serializers.CharField(
                        default='Страница не найдена.')
                },
            ),
        },
    ),
    'pay': extend_schema(
        description=('Обновляет статус заказа '
                     'с указанным идентификатором.'),
        summary='Оплатить заказ',
        request=None,
        responses={
            status.HTTP_202_ACCEPTED: inline_serializer(
                name='pay_202',
                fields={
                    'pay_status': serializers.CharField(default='bool')
                },
            ),
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='pay_error_401',
                fields={
                    'detail': serializers.CharField(
                        default='Учетные данные не были предоставлены.')
                },
            ),
            status.HTTP_404_NOT_FOUND: inline_serializer(
                name='pay_error_404',
                fields={
                    'detail': serializers.CharField(
                        default='Страница не найдена.')
                },
            ),
        }
    ),
    'rating': extend_schema(
        description=('Создает/Обновляет отзыв к заказу '
                     'с указанным идентификатором.'),
        summary='Создать/Обновить отзыв к заказу.',
        request=OrderRatingSerializer,
        responses={
            status.HTTP_200_OK: OrderRatingSerializer,
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                name='ratings_error_400',
                fields={
                    'detail': serializers.CharField(default='string')
                },
            ),
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='ratings_error_401',
                fields={
                    'detail': serializers.CharField(
                        default='Учетные данные не были предоставлены.')
                },
            ),
            status.HTTP_404_NOT_FOUND: inline_serializer(
                name='ratings_error_404',
                fields={
                    'detail': serializers.CharField(
                        default='Страница не найдена.')
                },
            ),
        },
    ),
    'get_available_time': extend_schema(
        description=('Получает доступную дату к заказу '
                     'с указанным идентификатором.'),
        summary='Получить доступную дату и время для заказа.',
        request=CleaningGetTimeSerializer,
        responses={
            status.HTTP_200_OK: inline_serializer(
                name='get_time_200',
                fields={
                    'detail': serializers.CharField(
                        default='Пока хз, что должно возвращать.')
                },
            ),
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                name='rating_error_400',
                fields={
                    'detail': serializers.CharField(default='string')
                },
            ),
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='rating_error_401',
                fields={
                    'detail': serializers.CharField(
                        default='Учетные данные не были предоставлены.')
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
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='rating_list_error_401',
                fields={
                    'detail': serializers.CharField(
                        default='Учетные данные не были предоставлены.')
                },
            ),
        },
    ),
    'retrieve': extend_schema(
        description=('Возвращает отзыв '
                     'с указанным идентификатором.'),
        summary='Получить отзыв.',
        responses={
            status.HTTP_200_OK: RatingSerializer,
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='rating_retrieve_error_401',
                fields={
                    'detail': serializers.CharField(
                        default='Учетные данные не были предоставлены.')
                },
            ),
            status.HTTP_404_NOT_FOUND: inline_serializer(
                name='rating_retrieve_error_404',
                fields={
                    'detail': serializers.CharField(
                        default='Страница не найдена.')
                },
            ),
        },
    ),
    'partial_update': extend_schema(
        description=('Обновляет отзыв '
                     'с указанным идентификатором.'),
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
                        default='Учетные данные не были предоставлены.')
                },
            ),
            status.HTTP_404_NOT_FOUND: inline_serializer(
                name='ratings_update_error_404',
                fields={
                    'detail': serializers.CharField(
                        default='Страница не найдена.')
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
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='service_list_error_401',
                fields={
                    'detail': serializers.CharField(
                        default='Учетные данные не были предоставлены.')
                },
            ),
            status.HTTP_403_FORBIDDEN: inline_serializer(
                name='service_list_error_403',
                fields={
                    'detail': serializers.CharField(
                        default='У вас недостаточно прав'
                        'для выполнения данного действия.')
                },
            ),
        },
    ),
    'create': extend_schema(
        description='Создает новый услугу.',
        summary='Создать новую услугу.',
        responses={
            status.HTTP_201_CREATED: CreateServiceSerializer,
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                name='service_create_error_400',
                fields={
                    'detail': serializers.CharField(default='string.')
                },
            ),
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='service_create_error_401',
                fields={
                    'detail': serializers.CharField(
                        default='Учетные данные не были предоставлены.')
                },
            ),
            status.HTTP_403_FORBIDDEN: inline_serializer(
                name='service_create_error_403',
                fields={
                    'detail': serializers.CharField(
                        default='У вас недостаточно прав'
                        'для выполнения данного действия.')
                },
            ),
        },
    ),
    'retrieve': extend_schema(
        description=('Возвращает услугу '
                     'с указанным идентификатором.'),
        summary='Получить услугу.',
        responses={
            status.HTTP_200_OK: GetServiceSerializer,
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='service_retrieve_error_401',
                fields={
                    'detail': serializers.CharField(
                        default='Учетные данные не были предоставлены.')
                },
            ),
            status.HTTP_403_FORBIDDEN: inline_serializer(
                name='service_retrieve_error_403',
                fields={
                    'detail': serializers.CharField(
                        default='У вас недостаточно прав'
                        'для выполнения данного действия.')
                },
            ),
            status.HTTP_404_NOT_FOUND: inline_serializer(
                name='service_retrieve_error_404',
                fields={
                    'detail': serializers.CharField(
                        default='Страница не найдена.')
                },
            ),
        },
    ),
    'update': extend_schema(
        description=('Обновляет услугу '
                     'с указанным идентификатором.'),
        summary='Обновить существующую услугу.',
        responses={
            status.HTTP_200_OK: GetServiceSerializer,
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                name='service_update_error_400',
                fields={
                    'detail': serializers.CharField(default='string')
                },
            ),
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='service_update_error_401',
                fields={
                    'detail': serializers.CharField(
                        default='Учетные данные не были предоставлены.')
                },
            ),
            status.HTTP_403_FORBIDDEN: inline_serializer(
                name='service_update_error_403',
                fields={
                    'detail': serializers.CharField(
                        default='У вас недостаточно прав'
                        'для выполнения данного действия.')
                },
            ),
            status.HTTP_404_NOT_FOUND: inline_serializer(
                name='service_update_error_404',
                fields={
                    'detail': serializers.CharField(
                        default='Страница не найдена.')
                },
            ),
        },
    ),
}

USER_SCHEMA = {
    'list': extend_schema(
        description='Возвращает список пользователей.',
        summary='Получить список пользователей.',
        responses={
            status.HTTP_200_OK: UserSerializer,
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='user_list_error_401',
                fields={
                    'detail': serializers.CharField(
                        default='Учетные данные не были предоставлены.')
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
                name='user_create_error_400',
                fields={
                    'detail': serializers.CharField(default='string.')
                },
            ),
        },
    ),
    'update': extend_schema(
        description=('Полностью обновляет пользователя '
                     'с указанным идентификатором.'),
        summary='Полностью обновить пользователя.',
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
                        default='Учетные данные не были предоставлены.')
                },
            ),
            status.HTTP_404_NOT_FOUND: inline_serializer(
                name='users_update_error_404',
                fields={
                    'detail': serializers.CharField(
                        default='Страница не найдена.')
                },
            ),
        },
    ),
    'partial_update': extend_schema(
        description=('Частично обновляет пользователя '
                     'с указанным идентификатором.'),
        summary='Частично обновить пользователя.',
        responses={
            status.HTTP_200_OK: UserSerializer,
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                name='user_update_error_400',
                fields={
                    'detail': serializers.CharField(default='string')
                },
            ),
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='user_update_error_401',
                fields={
                    'detail': serializers.CharField(
                        default='Учетные данные не были предоставлены.')
                },
            ),
            status.HTTP_404_NOT_FOUND: inline_serializer(
                name='user_update_error_404',
                fields={
                    'detail': serializers.CharField(
                        default='Страница не найдена.')
                },
            ),
        },
    ),
    'orders': extend_schema(
        description=('Список всех заказов пользователя '
                     'с указанным идентификатором.'),
        summary='Получить список всех заказов пользователя.',
        responses={
            status.HTTP_200_OK: OrderGetSerializer,
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='user_orders_list_error_401',
                fields={
                    'detail': serializers.CharField(
                        default='Учетные данные не были предоставлены.')
                },
            ),
        },
    ),
    'confirm_email': extend_schema(
        summary='Подтверждение электронной почты.',
        description='Подтверждение электронной почты.',
        responses={
            status.HTTP_200_OK: inline_serializer(
                name='user_email_200',
                fields={
                    'Token': serializers.CharField(default='string')
                },
            ),
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='user_email_error_401',
                fields={
                    'detail': serializers.CharField(
                        default='Учетные данные не были предоставлены.')
                },
            ),
        },
    ),
    'me': extend_schema(
        description=('Возвращает пользователя '
                     'с указанным идентификатором.'),
        summary='Получить авторизованного пользователя.',
        responses={
            status.HTTP_200_OK: UserSerializer,
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='me_error_401',
                fields={
                    'detail': serializers.CharField(
                        default='Учетные данные не были предоставлены.')
                },
            ),
            status.HTTP_403_FORBIDDEN: inline_serializer(
                name='me_error_403',
                fields={
                    'detail': serializers.CharField(
                        default='У вас недостаточно прав'
                        'для выполнения данного действия.')
                },
            ),
            status.HTTP_404_NOT_FOUND: inline_serializer(
                name='me_error_404',
                fields={
                    'detail': serializers.CharField(
                        default='Страница не найдена.')
                },
            ),
        },
    ),
}


"""Schema views token constant."""


TOKEN_CREATE_SCHEMA = {
    'description': 'Создает token авторизации.',
    'summary': 'Создать token авторизации.',
    'responses': {
        status.HTTP_201_CREATED: inline_serializer(
            name='token_create_201',
            fields={'Token': serializers.CharField(default='string')},
        ),
    },
}

TOKEN_DESTROY_SCHEMA = {
    'description': 'Удаляет token авторизации.',
    'summary': 'Удалить token авторизации.',
    'request': TokenDestroySchema,
    'responses': {
        status.HTTP_204_NO_CONTENT: inline_serializer(
            name='token_destroy_204',
            fields={'string': serializers.CharField(
                default='No response body')},
        ),
    },
}
