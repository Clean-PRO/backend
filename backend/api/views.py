# TODO: аннотировать типы данных. Везде. Абсолютно.
# TODO: Сделать хорошие docstring. Везде.

from django.db.models import QuerySet
from django.contrib.auth import authenticate
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.utils.serializer_helpers import ReturnDict
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)

from api.filters import FilterService
from api.permissions import (
    IsAdminOrReadOnly,
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
    PaySerializer,
    RatingSerializer,
    UserSerializer,
    UserRegisterSerializer,
)
from api.utils import create_password, get_available_time_json, send_mail
from cleanpro.app_data import (
    EMAIL_CONFIRM_EMAIL_SUBJECT, EMAIL_CONFIRM_EMAIL_TEXT, SERVICES_ADDITIONAL,
)
from .schemas_config import (
    TYPES_CLEANING_SCHEMA,
    MEASURE_SCHEMA,
    SERVICE_SCHEMA,
    RATING_SCHEMA,
    ORDER_SCHEMA,
    USER_SCHEMA,
)
from services.models import CleaningType, Measure, Order, Rating, Service
from services.signals import get_cached_reviews
from users.models import User


@extend_schema(tags=["Measure"])
@extend_schema_view(**MEASURE_SCHEMA)
class MeasureViewSet(viewsets.ModelViewSet):
    """Работа с единицами измерения услуг."""

    queryset = Measure.objects.all()
    serializer_class = MeasureSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None
    http_method_names = ('get', 'post', 'put',)


@extend_schema(tags=["Types cleaning"])
@extend_schema_view(**TYPES_CLEANING_SCHEMA)
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


@extend_schema(tags=["Service"])
@extend_schema_view(**SERVICE_SCHEMA)
class ServiceViewSet(viewsets.ModelViewSet):
    """Работа с услугами."""

    queryset = Service.objects.select_related('measure').all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = FilterService
    http_method_names = ('get', 'post', 'put',)

    def get_queryset(self):
        if not self.request.user.is_staff:
            return self.queryset.filter(service_type=SERVICES_ADDITIONAL)
        else:
            return self.queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetServiceSerializer
        else:
            return CreateServiceSerializer


@extend_schema(tags=["User"])
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
            return [permissions.AllowAny()]
        if self.request.method == 'GET':
            return [permissions.IsAdminUser()]
        return [IsOwnerOrAdmin()]

    @action(
        detail=True,
        url_path='orders',
        methods=('get',),
        permission_classes=(permissions.IsAdminUser,)
    )
    def orders(self, request, pk):
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
        url_path='me',
        methods=('get',),
        permission_classes=(permissions.IsAuthenticated,)
    )
    def me(self, request):
        instance: User = request.user
        serializer: UserSerializer = UserSerializer(instance)
        data: ReturnDict = serializer.data
        for attribute in ('is_staff', 'is_cleaner'):
            if getattr(self.request.user, attribute):
                data[attribute] = True
        return Response(data)

    @action(
        detail=False,
        url_path='confirm_email',
        methods=('post',),
        permission_classes=(permissions.AllowAny,)
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
        url_path='confirm_password',
        methods=('post',),
        permission_classes=(permissions.AllowAny,)
    )
    def confirm_password(self, request):
        """
        Если пользователь с указанно почтой существует: проверяет возможность
        авторизации с предоставленными данными.
        Если пользователя не существует - проверяет валидность указанного
        пароля и далее возможность авторизации.
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


@extend_schema(tags=["Order"])
@extend_schema_view(**ORDER_SCHEMA)
class OrderViewSet(viewsets.ModelViewSet):
    """Список заказов."""
    http_method_names = ('get', 'post', 'patch', 'put',)
    queryset = Order.objects.select_related('user', 'address',).all()

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (permissions.IsAuthenticated,)
        else:
            self.permission_classes = (IsOwnerOrAdmin,)
        return super().get_permissions()

    def get_queryset(self):
        if not self.request.user.is_staff:
            return self.queryset.filter(user=self.request.user)
        else:
            return self.queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrderGetSerializer
        if self.request.method in ('PATCH', 'PUT'):
            if self.request.user.is_staff:
                return AdminOrderPatchSerializer
            else:
                return OwnerOrderPatchSerializer
        return OrderPostSerializer

    @action(
        detail=True,
        methods=('post', 'put',),
        url_path='rating',
        permission_classes=(IsOwnerOrAdmin,)
    )
    def rating(self, request, pk):
        """Оценить заказ."""
        request.data['id'] = pk
        if request.method == 'POST':
            serializer = OrderRatingSerializer(
                data=request.data,
                context={'request': request},
            )
        if request.method == 'PUT':
            order = get_object_or_404(Order, id=pk)
            rating = get_object_or_404(Rating, order=order, user=request.user)
            serializer = OrderRatingSerializer(
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
        permission_classes=(IsOwnerAbleToPay,),
        url_path='pay',
    )
    def pay(self, request, pk):
        """Оплатить заказ."""
        serializer: serializers = self.__modify_order(
            order_id=pk,
            request=request,
            serializer_class=PaySerializer,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=('post',),
        url_path='get_available_time',
    )
    def get_available_time(self, request):
        serializer = CleaningGetTimeSerializer(data=request.data)
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

    def __modify_order(
            self,
            order_id,
            request: HttpRequest,
            serializer_class: serializers,
            ) -> serializers:  # noqa (E123)
        order = get_object_or_404(Order, id=order_id)
        request.data['id'] = order.id
        serializer = serializer_class(
            order,
            request.data,
            context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer


@extend_schema(tags=["Rating"])
@extend_schema_view(**RATING_SCHEMA)
class RatingViewSet(viewsets.ModelViewSet):
    """Список отзывов."""
    queryset = Rating.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = RatingSerializer
    http_method_names = ('get', 'patch',)
    pagination_class = LimitOffsetPagination

    def list(self, request, *args, **kwargs):
        cached_reviews: list[dict] = get_cached_reviews()
        limit: int = request.query_params.get('limit')
        if limit and cached_reviews:
            try:
                cached_reviews: list[dict] = cached_reviews[:int(limit)]
            except ValueError:
                raise serializers.ValidationError(
                    detail="Invalid limit value. Limit must be an integer.",
                    code=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            data=cached_reviews,
            status=status.HTTP_200_OK,
        )

    def perform_create(self, serializer):
        order_id = self.kwargs.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        serializer.save(user=self.request.user, order=order)
        return
