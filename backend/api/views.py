# TODO: аннотировать типы данных. Везде. Абсолютно.
# TODO: Сделать хорошие docstring. Везде.

from django.db.models import QuerySet
from django.contrib.auth import authenticate
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.utils.serializer_helpers import ReturnDict
from drf_spectacular.utils import extend_schema_view, extend_schema
from djoser.views import TokenCreateView, TokenDestroyView

from api.filters import FilterService
from api.permissions import (
    IsAdminOrReadOnly,
    IsCurrentUserOrAdmin,
    IsOwnerOrAdmin,
    IsOwnerAbleToPay,
)
from api.serializers import (
    AdminOrderPatchSerializer,
    CleaningGetTimeSerializer,
    CreateCleaningTypeSerializer,
    CreateServiceSerializer,
    EmailVerifySerializer,
    GetCleaningTypeSerializer,
    GetServiceSerializer,
    MeasureSerializer,
    OrderGetSerializer,
    OrderPostSerializer,
    OrderRatingSerializer,
    OwnerOrderPatchSerializer,
    PasswordConfirmSerializer,
    RatingSerializer,
    UserSerializer,
    UserRegisterSerializer,
)
from api.utils import create_password, get_available_time_json, send_mail
from cleanpro.app_data import (
    CACHE_LIST_RESPONSE_RATINGS,
    EMAIL_CONFIRM_EMAIL_SUBJECT, EMAIL_CONFIRM_EMAIL_TEXT,
    ORDER_ACCEPTED_STATUS, ORDER_CANCELLED_STATUS, ORDER_FINISHED_STATUS,
    SERVICES_ADDITIONAL,
)
from cleanpro.settings import CACHE_TIMEOUT_SEC
from .schemas_views import (
    CLEANING_TYPES_SCHEMA,
    TOKEN_DESTROY_SCHEMA,
    TOKEN_CREATE_SCHEMA,
    MEASURE_SCHEMA,
    SERVICE_SCHEMA,
    RATING_SCHEMA,
    ORDER_SCHEMA,
    USER_SCHEMA,
)
from services.models import CleaningType, Measure, Order, Rating, Service
from users.models import User


# TODO: Метод PUT требует все поля. Исправить.
@extend_schema_view(**CLEANING_TYPES_SCHEMA)
class CleaningTypeViewSet(viewsets.ModelViewSet):
    """Работа с наборами услуг."""

    queryset = CleaningType.objects.prefetch_related('service').all()
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None
    http_method_names = ('get', 'post', 'put')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetCleaningTypeSerializer
        else:
            return CreateCleaningTypeSerializer


@extend_schema_view(**MEASURE_SCHEMA)
class MeasureViewSet(viewsets.ModelViewSet):
    """Работа с единицами измерения услуг."""

    queryset = Measure.objects.all()
    serializer_class = MeasureSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None
    http_method_names = ('get', 'post', 'put', 'delete')


@extend_schema_view(**ORDER_SCHEMA)
class OrderViewSet(viewsets.ModelViewSet):
    """Работа с заказами."""

    http_method_names = ('get', 'post', 'put',)

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (permissions.IsAuthenticated,)
        else:
            self.permission_classes = (IsOwnerOrAdmin,)
        if self.action == 'rating':
            self.permission_classes = (IsOwnerOrAdmin,)
        elif self.action == 'pay':
            self.permission_classes = (IsOwnerAbleToPay,)
        elif self.action == 'get_available_time':
            self.permission_classes = (permissions.AllowAny,)
        return super().get_permissions()

    def get_queryset(self):
        if not self.request.user.is_staff:
            return Order.objects.select_related(
                'user',
                'address',
            ).filter(
                user=self.request.user,
            )
        else:
            return Order.objects.select_related('user', 'address',).all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrderGetSerializer
        if self.request.method == 'POST':
            return OrderPostSerializer
        # TODO: проверить работу, переименовать сериализаторы
        if self.request.user.is_staff:
            return AdminOrderPatchSerializer
        return OwnerOrderPatchSerializer

    # TODO: разобраться с логикой создать/обновить.
    # TODO: проверить при развертке документацию.
    @action(
        detail=True,
        methods=('post', 'put',),
        url_path='rating',
    )
    def rating(self, request, pk):
        """Оценить заказ."""
        # TODO: непонятный момент. Посмотреть позже.
        request.data['id']: int = pk
        if request.method == 'POST':
            serializer = OrderRatingSerializer(
                data=request.data,
                context={'request': request},
            )
        if request.method == 'PUT':
            order: Order = get_object_or_404(Order, id=pk)
            rating: Rating = get_object_or_404(
                Rating, order=order, user=request.user
            )
            serializer: serializers = OrderRatingSerializer(
                instance=rating,
                data=request.data,
                context={'request': request},
            )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=('post',),
        url_path='pay',
    )
    def pay(self, request, pk):
        """Оплатить заказ."""
        order: Order = self.get_object()
        status_code: status = status.HTTP_400_BAD_REQUEST
        if order.order.status in (ORDER_ACCEPTED_STATUS, ORDER_FINISHED_STATUS):  # noqa (E501)
            data_status: str = 'Заказ уже оплачен.'
        elif order.order.status == ORDER_CANCELLED_STATUS:
            data_status: str = 'Заказ был отменен.'
        else:
            order.status: str = ORDER_ACCEPTED_STATUS
            order.save()
            data_status: str = 'Заказ оплачен.'
            status_code: status = status.HTTP_200_OK
        return Response(
            data={'status': data_status},
            status=status_code
        )

    @action(
        detail=False,
        methods=('post',),
        url_path='get_available_time',
    )
    def get_available_time(self, request):
        """Получить список доступных часов для бронирования заказа."""
        serializer: serializers = CleaningGetTimeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            data=get_available_time_json(
                cleaning_date=serializer.validated_data['cleaning_date'],
                total_time=serializer.validated_data['total_time'],
            ),
            status=status.HTTP_200_OK,
        )


@extend_schema_view(**RATING_SCHEMA)
class RatingViewSet(viewsets.ModelViewSet):
    """Список отзывов."""

    queryset = Rating.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = RatingSerializer
    http_method_names = ('get', 'patch',)
    pagination_class = LimitOffsetPagination

    def list(self, request, *args, **kwargs):
        # TODO: учесть запрос с limit для главной страницы
        cached_data: Response = cache.get(CACHE_LIST_RESPONSE_RATINGS)
        if cached_data:
            return Response(cached_data)
        response: Response = super().list(request, *args, **kwargs)
        cache.set(
            key=CACHE_LIST_RESPONSE_RATINGS,
            value=response.data,
            timeout=CACHE_TIMEOUT_SEC,
        )
        return response

    def perform_create(self, serializer):
        order_id: int = self.kwargs.get('order_id')
        order: Order = get_object_or_404(Order, id=order_id)
        serializer.save(user=self.request.user, order=order)
        return


# TODO: Метод PUT требует всех полей. Исправить.
@extend_schema_view(**SERVICE_SCHEMA)
class ServiceViewSet(viewsets.ModelViewSet):
    """Работа с услугами."""

    queryset = Service.objects.select_related('measure').all()
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = FilterService
    http_method_names = ('get', 'post', 'put',)

    def get_queryset(self):
        if not self.request.user.is_staff:
            self.pagination_class: None = None
            return self.queryset.filter(service_type=SERVICES_ADDITIONAL)
        else:
            return self.queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetServiceSerializer
        else:
            return CreateServiceSerializer


@extend_schema(**TOKEN_CREATE_SCHEMA)
class TokenCreateSchemaView(TokenCreateView):
    pass


@extend_schema(**TOKEN_DESTROY_SCHEMA)
class TokenDestroySchemaView(TokenDestroyView):
    pass


# TODO: НЕ ВАЛИДИРУЕТСЯ ПОЧТА!!!
# TODO: метод PUT требует все поля. Исправить.
@extend_schema_view(**USER_SCHEMA)
class UserViewSet(viewsets.ModelViewSet):
    """Работа с пользователями."""

    queryset = User.objects.select_related('address').all()
    http_method_names = ('get', 'post', 'put',)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserRegisterSerializer
        return UserSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (permissions.AllowAny,)
        elif self.request.method == 'GET':
            self.permission_classes = (permissions.IsAdminUser,)
        else:
            self.permission_classes = (IsCurrentUserOrAdmin,)
        if self.action == 'me':
            self.permission_classes = (permissions.IsAuthenticated,)
        elif self.action in ('confirm_email', 'confirm_password'):
            self.permission_classes = (permissions.AllowAny,)
        return super().get_permissions()

    @action(
        detail=True,
        methods=('get',),
        url_path='orders',
    )
    def orders(self, request, pk):
        """Возвращает список заказов авторизированного пользователя."""
        queryset = Order.objects.filter(
            user=pk,
        ).select_related(
            'user',
            'cleaning_type',
            'address',
        )
        page = self.paginate_queryset(queryset)
        serializer = OrderGetSerializer(
            page,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=False,
        methods=('get',),
        url_path='me',
    )
    def me(self, request):
        """Возвращает данные авторизированного пользователя."""
        instance: User = request.user
        serializer: UserSerializer = UserSerializer(instance)
        data: ReturnDict = serializer.data
        for attribute in ('is_staff', 'is_cleaner'):
            if getattr(self.request.user, attribute):
                data[attribute] = True
        return Response(data)

    @action(
        detail=False,
        methods=('post',),
        url_path='confirm_email',
    )
    def confirm_email(self, request):
        """
        Производит валидацию введенного email и производит проверку
        существования пользователя с указанной почтой.
        Если пользователя не существует: генерирует уникальный пароль
        учетной записи для авторизации на сайте при осуществлении заказа.
        """
        serializer: serializers = EmailVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email: str = serializer.validated_data.get('email')
        if User.objects.filter(email=email).exists():
            data: dict[str, str] = {
                'exists': 'Введите пароль вашей учетной записи:',
            }
        else:
            new_password: str = create_password(email=email)
            send_mail(
                subject=EMAIL_CONFIRM_EMAIL_SUBJECT,
                message=EMAIL_CONFIRM_EMAIL_TEXT.format(password=new_password),
                to=(email,)
            )
            data: dict[str, str] = {
                'created': (
                    'Введите пароль вашей учетной записи, '
                    'который был выслан на указанную почту:'
                ),
            }
        return Response(
            data=data,
            status=status.HTTP_200_OK,
        )

    @action(
        detail=False,
        methods=('post',),
        url_path='confirm_password',
    )
    def confirm_password(self, request):
        """
        Проверяет возможность авторизации с предоставленными данными.
        Если пользователя с указанно почтой не существует - сначала проверяет
        валидность указанного пароля.
        """
        serializer: serializers = PasswordConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email: str = serializer.validated_data.get('email')
        password: str = serializer.validated_data.get('password')
        user: QuerySet = User.objects.filter(email=email)
        if not user.exists() and password == create_password(email=email):
            user: User = User.objects.create(email=email)
            user.set_password(password)
            user.save()
        else:
            user: User = user.first()
        authentication: User = authenticate(
            email=email,
            password=password
        )
        if authentication is None:
            data: dict = {'password': 'Указан неверный пароль.'}
            status_code: status = status.HTTP_400_BAD_REQUEST
        else:
            data: dict = {'password': 'Пароль успешно подтвержден.'}
            status_code: status = status.HTTP_200_OK
        return Response(data=data, status=status_code)
