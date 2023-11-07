# TODO: аннотировать типы данных. Везде. Абсолютно.

from django.http import HttpRequest
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
from api.mixin import CreateUpdateListSet
from api.permissions import (
    IsAdminOrReadOnly,
    IsNotAdmin,
    IsOwner,
)
from api.serializers import (
    AdminOrderPatchSerializer,
    CleaningGetTimeSerializer,
    CreateCleaningTypeSerializer,
    CreateServiceSerializer,
    EmailConfirmSerializer,
    GetCleaningTypeSerializer,
    GetServiceSerializer,
    MeasureSerializer,
    OrderGetSerializer,
    OrderPostSerializer,
    OrderRatingSerializer,
    OwnerOrderPatchSerializer,
    PaySerializer,
    RatingSerializer,
    UserCreateSerializer,
    UserGetSerializer,
)
from api.utils import generate_code, get_available_time_json, send_mail
from cleanpro.app_data import (
    EMAIL_CONFIRM_CODE_TEXT, EMAIL_CONFIRM_CODE_SUBJECT,
)
from .schemas_views import (
    CLEANING_TYPES_SCHEMA,
    TOKEN_DESTROY_SHEMA,
    TOKEN_CREATE_SHEMA,
    MEASURE_SCHEMA,
    SERVICE_SCHEMA,
    RATING_SCHEMA,
    ORDER_SCHEMA,
    USER_SCHEMA,
)
from cleanpro.settings import ADDITIONAL_CS
from services.models import CleaningType, Measure, Order, Rating, Service
from services.signals import get_cached_reviews
from users.models import User


@extend_schema_view(**CLEANING_TYPES_SCHEMA)
class CleaningTypeViewSet(viewsets.ModelViewSet):
    """Работа с типами услуг."""
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
    permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly)
    pagination_class = None
    http_method_names = ('get', 'post', 'put', 'delete')


@extend_schema_view(**ORDER_SCHEMA)
class OrderViewSet(viewsets.ModelViewSet):
    """Список заказов."""
    http_method_names = ('get', 'post', 'put',)
    queryset = Order.objects.select_related('user', 'address',).all()
    # TODO: лишний код. Можно оставить permission_classes на уровне проекта
    #       и переписать get_permissions(self)
    permission_classes = (IsOwner,)

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (permissions.AllowAny,)
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

    def __modify_order(
            self,
            order_id,
            request: HttpRequest,
            serializer_class: serializers,
            ) -> serializers:  # NoQa
        order = get_object_or_404(Order, id=order_id)
        request.data['id'] = order.id
        serializer = serializer_class(
            order,
            request.data,
            context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer

    @action(
        detail=True,
        methods=('post', 'put',),
        url_path='rating',
    )
    def rating(self, request, pk):
        """Оценить заказ."""
        order = get_object_or_404(Order, id=pk)
        request.data['id'] = order.id
        if request.method == 'POST':
            serializer = OrderRatingSerializer(
                data=request.data,
                context={'request': request},
            )
            if serializer.is_valid(raise_exception=True):
                serializer.validated_data['user'] = request.user
                serializer.validated_data['order'] = order
                serializer.save()
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'PUT':
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
        # TODO: сделать разрешение только создателю заказа.
        #       Можно без администратора, мысль здравая.
        permission_classes=(IsNotAdmin,),
        url_path='pay',
    )
    def pay(self, request, pk):
        """Оплатить заказ."""
        serializer: serializers = self.__modify_order(
            order_id=pk,
            request=request,
            serializer_class=PaySerializer,
        )
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

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
            self.pagination_class = None
            return self.queryset.filter(service_type=ADDITIONAL_CS)
        else:
            return self.queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetServiceSerializer
        else:
            return CreateServiceSerializer


@extend_schema_view(**USER_SCHEMA)
class UserViewSet(CreateUpdateListSet):
    queryset = User.objects.select_related('address').all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserGetSerializer

    @action(
        detail=True,
        url_path='orders',
        methods=('get',),
        permission_classes=(permissions.IsAdminUser,)
    )
    def orders(self, request, pk):
        queryset = Order.objects.filter(
            user=pk
        ).select_related('user', 'cleaning_type', 'address')
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
        permission_classes=(permissions.IsAuthenticated,)
    )
    def me(self, request):
        instance: User = request.user
        serializer: UserGetSerializer = UserGetSerializer(instance)
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
        serializer: serializers = EmailConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirm_code: str = generate_code()
        send_mail(
            subject=EMAIL_CONFIRM_CODE_SUBJECT,
            message=EMAIL_CONFIRM_CODE_TEXT.format(confirm_code=confirm_code),
            to=(serializer.validated_data.get('email'),),
        )
        return Response(
            data={"confirm_code": confirm_code},
            status=status.HTTP_200_OK,
        )


@extend_schema(**TOKEN_CREATE_SHEMA)
class TokenCreateShemaView(TokenCreateView):
    pass


@extend_schema(**TOKEN_DESTROY_SHEMA)
class TokenDestroyShemaView(TokenDestroyView):
    pass
