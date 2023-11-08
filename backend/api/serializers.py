import random
import re
from datetime import datetime

from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer  # noqa (E501)
from django.db import transaction
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from drf_base64.fields import Base64ImageField
from drf_spectacular.utils import extend_schema_serializer
from phonenumber_field.phonenumber import PhoneNumber
from rest_framework import serializers, status
from rest_framework.validators import UniqueValidator

from api.schemas_serializer import (
    ORDER_POST_SERIALIZER_SCHEMA, ORDER_RATING_SERIALIZER_SCHEMA,
    RATING_SERIALIZER_SCHEMA,
)
from api.utils import (
    get_or_create_address, get_available_cleaners,
)
from cleanpro.app_data import ORDER_CANCELLED_STATUS
from services.models import (
    Address, CleaningType, Measure, Order, Rating, Service, ServicesInOrder
)
from users.models import User
from users.validators import (
    ValidationError,
    validate_email, validate_password,
    EMAIL_PATTERN, USERNAME_PATTERN
)


class AddressSerializer(serializers.ModelSerializer):
    """Сериализатор адреса."""

    class Meta:
        model = Address
        fields = (
            'id',
            'city',
            'street',
            'house',
            'floor',
            'entrance',
            'apartment',
        )


class CleaningGetTimeSerializer(serializers.Serializer):
    """Сериализатор для запроса проверки доступного времени записи."""

    cleaning_date = serializers.DateField()
    total_time = serializers.IntegerField()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей."""
    address = AddressSerializer()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'phone',
            'address',
        )

    def update(self, instance, validated_data):
        """Производит обновление данных о пользователе и его адресе."""
        address_values = validated_data.pop('address')
        super().update(instance, validated_data)
        instance.address = get_or_create_address(
            address_data=address_values
        )
        instance.save()
        return instance


class UserRegisterSerializer(DjoserUserCreateSerializer):
    """Сериализатор для регистрации пользователей."""

    email = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message=(
                    'Пользователь с таким адресом электронной почты '
                    'уже зарегистрирован.'
                ),
            ),
        ],
    )

    class Meta:
        model = User
        fields = (
            'email',
            'password',
        )


class EmailVerifySerializer(serializers.Serializer):
    """Сериализатор проверки корректности email."""

    email = serializers.EmailField()

    def validate_email(self, value):
        """Производит валидацию поля email."""
        try:
            validate_email(value)
        except ValidationError as err:
            raise serializers.ValidationError(
                detail=err,
                code=status.HTTP_400_BAD_REQUEST,
            )
        return value


class PasswordConfirmSerializer(serializers.ModelSerializer):
    """Сериализатор проверки корректности email и password."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'phone',
            'password',
        )

    def validate_email(self, value):
        """Производит валидацию поля email."""
        try:
            validate_email(value)
        except ValidationError as err:
            raise serializers.ValidationError(
                detail=err,
                code=status.HTTP_400_BAD_REQUEST,
            )
        return value

    def validate_password(self, value):
        """Производит валидацию поля password."""
        try:
            validate_password(value)
        except ValidationError as err:
            raise serializers.ValidationError(
                detail=err,
                code=status.HTTP_400_BAD_REQUEST,
            )
        return value


class MeasureSerializer(serializers.ModelSerializer):
    """Сериализатор единиц измерения"""

    class Meta:
        model = Measure
        fields = (
            'id',
            'title',
        )


class GetServiceSerializer(serializers.ModelSerializer):
    """Сериализатор услуг"""

    image = Base64ImageField(read_only=True)
    measure = serializers.ReadOnlyField(
        source='measure.title',
        read_only=True,
    )

    class Meta:
        model = Service
        fields = (
            'id',
            'title',
            'price',
            'measure',
            'image',
            'cleaning_time',
        )


class CreateServiceSerializer(serializers.ModelSerializer):
    """Сериализатор создания и изменения услуг"""

    image = Base64ImageField(allow_null=True)
    measure = serializers.PrimaryKeyRelatedField(
        queryset=Measure.objects.all()
    )

    class Meta:
        model = Service
        fields = (
            'id',
            'title',
            'price',
            'measure',
            'image',
            'service_type',
            'cleaning_time',
        )

    def to_representation(self, value):
        representation = super().to_representation(value)

        representation['measure'] = value.measure.title
        return representation


class GetCleaningTypeSerializer(serializers.ModelSerializer):
    """Сериализатор набора услуг."""

    service = GetServiceSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = CleaningType
        fields = (
            'id',
            'title',
            'coefficient',
            'service',
        )


class CreateCleaningTypeSerializer(serializers.ModelSerializer):
    """Сериализатор создания и изменения наборов услуг"""

    service = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Service.objects.select_related('measure').all(),
    )

    class Meta:
        model = CleaningType
        fields = (
            'id',
            'title',
            'coefficient',
            'service',
        )

    def create(self, validated_data):
        services = validated_data.pop('service')
        cleaning_type = super().create(validated_data)
        cleaning_type.service.set(services)
        return cleaning_type

    def update(self, instance, validated_data):
        services = validated_data.pop('service')
        super().update(instance, validated_data)
        if services:
            instance.service.set(services)
        instance.save()
        return instance

    def to_representation(self, value):
        request = self.context.get('request')
        return GetCleaningTypeSerializer(
            value,
            context={'request': request}
        ).data


class ServicesInOrderSerializer(serializers.ModelSerializer):
    """Сериализатор перечня услуг в заказе."""

    id = serializers.ReadOnlyField(source='service.id')
    title = serializers.ReadOnlyField(source='service.title')
    measure = serializers.ReadOnlyField(source='service.measure.title')
    price = serializers.ReadOnlyField(source='service.price')
    image = Base64ImageField(source='service.image')

    class Meta:
        model = ServicesInOrder
        fields = (
            'id',
            'title',
            'measure',
            'price',
            'image',
            'amount',
        )


class OrderGetSerializer(serializers.ModelSerializer):
    """Сериализатор для представления заказа."""

    user = UserSerializer(read_only=True)
    address = AddressSerializer(read_only=True)
    cleaning_type = GetCleaningTypeSerializer(read_only=True)
    services = ServicesInOrderSerializer(
        source='services_in_order',
        many=True,
        read_only=True,
    )

    class Meta:
        model = Order
        fields = (
            'id',
            'user',
            'total_sum',
            'total_time',
            'comment',
            'comment_cancel',
            'order_status',
            'cleaning_type',
            'services',
            'rooms_number',
            'bathrooms_number',
            'pay_status',
            'address',
            'creation_date',
            'creation_time',
            'cleaning_date',
            'cleaning_time',
        )


@extend_schema_serializer(**ORDER_POST_SERIALIZER_SCHEMA)
class OrderPostSerializer(serializers.ModelSerializer):
    """Сериализатор для создания заказа."""

    # INFO: нельзя использовать CustomUserSerializer по причине того,
    #       Django будет проверять поля на уникальность и не позволит
    #       новому пользователю создать заказ.
    user = serializers.DictField(child=serializers.CharField())
    services = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )
    address = AddressSerializer()

    class Meta:
        model = Order
        fields = (
            'user',
            'total_sum',
            'total_time',
            'comment',
            'cleaning_type',
            'services',
            'rooms_number',
            'bathrooms_number',
            'address',
            'creation_date',
            'creation_time',
            'cleaning_date',
            'cleaning_time',
        )

    # TODO: сделать валидацию данных номера телефона и email
    def validate_user(self, user_data):
        """Производит валидацию данных о пользователе."""
        invalid_data: list[str] = []
        username: str = user_data.get('username', 'None')
        email: str = user_data.get('email', 'None')
        phone: str = user_data.get('phone', 'None')
        if not re.fullmatch(USERNAME_PATTERN, username):
            invalid_data.append("username")
        if not re.fullmatch(EMAIL_PATTERN, email):
            invalid_data.append("email")
        if not self.__validate_phone(phone):
            invalid_data.append("phone")
        if invalid_data:
            raise serializers.ValidationError(
                'Отсутствуют или указаны невалидные данные: '
                f'{", ".join(invalid_data)}.'
            )
        return user_data

    def validate_services(self, services_data):
        """Производит валидацию сервисов и их количества в заказе."""
        all_services_id: list[int] = [
            service.id for service in Service.objects.all()
        ]
        invalidated_services: list[int] = []
        for service in services_data:
            service_id: str = service.get('id')
            amount: str = service.get('amount')
            if service_id is None or amount is None:
                raise serializers.ValidationError(
                    'Укажите id и amount сервиса.'
                )
            if int(service_id) not in all_services_id or int(amount) <= 0:
                invalidated_services.append(service_id)
        if invalidated_services:
            raise serializers.ValidationError(
                'Убедитесь, что услуги со следующими id существуют, '
                'и для них указано валидное значение поля amount: '
                f'{", ".join(id for id in invalidated_services)}.'
            )
        return services_data

    def validate_total_sum(self, total_sum_data):
        # TODO: добавить проверку валидности стоимости заказа,
        #       чтобы его не подменили.
        return total_sum_data

    @transaction.atomic
    def create(self, data):
        """
        Создает новый заказ.
        Если пользователь отсутствует в базе данных - создает нового.
        Если адрес отсутствует в базе данных - создает новый.
        Если заказ уже был создан - возвращает ошибку 400.
        """
        random_cleaner: User = self.__get_random_cleaner(data=data)
        address: Address = get_or_create_address(
            address_data=data.get('address')
        )
        user_data: dict[str, str] = data.get('user', {})
        user: User = self.context['request'].user
        self.__check_user_data(
            address=address, user=user, user_data=user_data
        )
        order, is_created = Order.objects.get_or_create(
            user=user,
            total_sum=data.get('total_sum'),
            total_time=data.get('total_time'),
            comment=data.get('comment'),
            cleaning_type=data.get('cleaning_type'),
            rooms_number=data.get('rooms_number'),
            bathrooms_number=data.get('bathrooms_number'),
            address=address,
            cleaning_date=data.get('cleaning_date'),
            cleaning_time=data.get('cleaning_time'),
        )
        if not is_created:
            raise serializers.ValidationError(
                {"Статус": "Заказ уже был создан."}
            )
        order.cleaner: User = random_cleaner
        order.save()
        self.__services_bulk_create(order, data.get('services'))
        return order

    def to_representation(self, instance):
        return {'Статус': 'Заказ создан.'}

    def __check_user_data(
            self, address: Address, user: User, user_data: dict
            ) -> None:  # noqa E125
        """
        Проверяет данные пользователя:
            - если отсутствует значения полей username / phone: присваиваются
              соответствующие данные из user_data
            - если отсутствует ссылка на адрес: присваивается объект Address
        """
        if not user.phone:
            user.phone = user_data.get('phone')
        if not user.username:
            user.username = user_data.get('username')
        user.address = address if user.address is None else user.address
        user.save()
        return

    def __get_random_cleaner(self, data) -> User:
        """
        Проверяет наличие доступных уборщиков для указанного дня и времени
        заказа. Возвращает случайного из всех доступных.

        Если доступных уборщиков нет, вызывает ValidationError.
        """
        cleaner: QuerySet = get_available_cleaners(
            cleaning_date=data.get('cleaning_date'),
            cleaning_time=data.get('cleaning_time'),
            total_time=data.get('total_time'),
        )
        if cleaner.count() == 0:
            raise serializers.ValidationError(
                'Для указанного дня и времени нет доступных уборщиков.'
            )
        return random.choice(list(cleaner))

    def __services_bulk_create(self, order, services) -> None:
        """Добавляет сервисы в заказ."""
        ing_objs = []
        for item in services:
            id: str = item.get('id')
            amount: str = item.get('amount')
            service = Service.objects.get(id=int(id))
            ing_objs.append(
                ServicesInOrder(
                    order=order,
                    service=service,
                    amount=int(amount)
                )
            )
        ServicesInOrder.objects.bulk_create(ing_objs)
        return

    def __validate_phone(self, phone_data) -> PhoneNumber:
        """Производит валидацию номера телефона.
        Возвращает False, в случае ошибки валидации."""
        try:
            parsed_phone = PhoneNumber.from_string(phone_data)
            if parsed_phone.is_valid():
                return phone_data
        except Exception:
            pass
        return False


class OwnerOrderPatchSerializer(serializers.ModelSerializer):
    """Сериализатор для частичного изменения данных заказа владельцем."""

    class Meta:
        model = Order
        fields = (
            'order_status',
            'comment_cancel',
            'comment',
            'cleaning_date',
            'cleaning_time',
        )

    def validate(self, data):
        if not data:
            raise serializers.ValidationError(
                'Среди указанных полей нет ни '
                'одного разрешенного для редактирования.')
        if (data.get('order_status') and
                not data.get('order_status') == ORDER_CANCELLED_STATUS
                ):  # noqa (E124)
            raise serializers.ValidationError(
                'Вы можете установить только статус отмены заказа.')
        return data

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        if 'comment_cancel' in validated_data:
            instance.order_status = 'cancelled'
            instance.cancel_date: datetime = datetime.today().date()
            instance.cancel_time: datetime = datetime.today().time()
        instance.save()
        return instance

    def to_representation(self, value):
        return OrderGetSerializer(
            value,
            context={'request': self.context.get('request',)}
        ).data


class AdminOrderPatchSerializer(OwnerOrderPatchSerializer):
    """Сериализатор для частичного изменения данных заказа админом."""

    class Meta:
        model = Order
        fields = (
            'order_status',
            'pay_status',
            'comment_cancel',
            'comment',
            'cleaning_date',
            'cleaning_time',
        )

    def validate(self, data):
        if not data:
            raise serializers.ValidationError(
                'Среди указанных полей нет ни '
                'одного разрешенного для редактирования.')
        return data

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        if ('comment_cancel' not in validated_data and
                not validated_data.get('order_status') ==
                ORDER_CANCELLED_STATUS):
            instance.comment_cancel = None
            instance.cancel_date = None
            instance.cancel_time = None
        instance.save()
        return instance


@extend_schema_serializer(**RATING_SERIALIZER_SCHEMA)
class RatingSerializer(serializers.ModelSerializer):
    """
    Сериализатор для представления отзыва на уборку на главной странице.
    """

    user = UserSerializer(read_only=True)

    class Meta:
        fields = (
            'id',
            'username',
            'user',
            'order',
            'pub_date',
            'text',
            'score',
        )
        model = Rating
        read_only_fields = (
            'id',
            'username',
        )

    def to_representation(self, instance):
        data: dict[str, any] = super().to_representation(instance)
        for field in ('user', 'order'):
            data.pop(field, None)
        return data


@extend_schema_serializer(**ORDER_RATING_SERIALIZER_SCHEMA)
class OrderRatingSerializer(RatingSerializer):
    """
    Сериализатор для создания/изменения отзыва на уборку в приложении.
    """

    # TODO: излишний код валидации, посмотреть позже.
    def validate(self, data):
        request: dict[str, any] = self.context.get('request')
        user: User = request.user
        order_id: int = request.data.get('id',)
        order: Order = get_object_or_404(Order, id=order_id)
        if order.order_status != 'finished':
            raise serializers.ValidationError(
                'Изменить отзыв на незавершенный заказ невозможно.')
        if Rating.objects.filter(order=order, user=user).exists():
            raise serializers.ValidationError(
                'Отзыв на этот заказ вы уже оставляли.')
        return data

    # TODO: излишний код создания, посмотреть позже.
    def create(self, validated_data):
        request: dict[str, any] = self.context.get('request')
        order_id: int = request.data.get('id',)
        order: Order = get_object_or_404(Order, id=order_id)
        rating: Rating = super().create(validated_data)
        rating.user: User = request.user
        rating.order: Order = order
        rating.save()
        return rating
