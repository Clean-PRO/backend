from rest_framework.permissions import SAFE_METHODS
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import make_password
from django.core import mail
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from api.serializers import CustomUserSerializer
from djoser.views import UserViewSet
from rest_framework import viewsets, status
from rest_framework import permissions
from .permissions import (IsOwnerOrReadOnly, IsOwner)
from service.models import Order, Rating
from users.models import User
from .serializers import (PostOrderSerializer,
                          GetOrderSerializer,
                          CommentSerializer,
                          DateTimeSerializer,
                          RatingSerializer,
                          OrderStatusSerializer,
                          ConfirmMailSerializer,
                          PaySerializer,
                          CancellSerializer)


# TODO: к отредактированным импортам согласно PEP8
from cleanpro.settings import DEBUG
# TODO: создать core для сайта, перенести туда часть настроек из settings.py,
# перенести это, сделать там смысловое разделение с указанием блоков.

# TODO: Добавить URL сайта из переменных окружения с указанием эндпоинта
PASSWORD_RESET_LINK: str = None

EMAIL_CONFIRM_SUBJECT: str = 'Welcome to CleanPro!'
EMAIL_CONFIRM_TEXT: str = (
    'Dear {username},\n'
    '\n'
    'Welcome to CleanPro! We are thrilled to have you as part '
    'of our community.\n'
    '\n'
    'You have successfully confirmed your email, and now you have '
    'full access to your account.\n'
    '\n'
    'Below, you will find your account details:\n'
    '\n'
    'Username: {username}\n'
    'Password: {password}\n'
    '\n'
    'Please keep this information in a secure place. '
    'If you ever forget your password, you can reset it by following this '
    f'link: {PASSWORD_RESET_LINK}''\n'
    '\n'
    'If you have any questions or need further assistance, do not hesitate '
    f'to reach out to us at {settings.DEFAULT_FROM_EMAIL}.''\n'
    '\n'
    'Thank you for choosing CleanPro! We hope you enjoy your time with us '
    'and wish you a pleasant experience.\n'
    '\n'
    'Best regards,\n'
    'The CleanPro Team'
)


# TODO: аннотировать типы данных. Везде. Абсолютно.
def send_mail(subject: str, message: str, to: tuple[str]) -> None:
    """Отправляет электронное сообщение.
    "backend=None" означает, что бекенд будет выбран согласно указанному
    значению в settings.EMAIL_BACKEND."""
    with mail.get_connection(backend=None, fail_silently=False) as conn:
        mail.EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=to,
            connection=conn
        ).send(fail_silently=False)
    return


class UserViewSet(UserViewSet):
    """Список пользователей."""
    serializer_class = CustomUserSerializer

    @action(
        detail=True,
        methods=['get', ],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def orders(self, request, id):
        """Список заказов пользователя."""
        queryset = Order.objects.filter(user=id)
        page = self.paginate_queryset(queryset)
        serializer = GetOrderSerializer(page, many=True,
                                            context={'request': request})
        return self.get_paginated_response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def confirm_mail(request):
    """Подтвердить электронную почту."""
    serializer = ConfirmMailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User, email=serializer.validated_data.get('email')
    )
    # TODO: разобраться, с со строкой кода ниже.
    # Пароль сам генерируется? Еще и в виде токена?? Что это вообще такое?
    # Для установки пароля используется метод .set_password()
    # Только пользователь сам себе ставит пароль при регистрации.
    # Если это попытка а-ля "хешировать" пароль - Django сам это делает.
    # TODO: адекватная практика на мой взгляд: при регистрации делать
    # пользователя с параметром "is.active=False" и при подтверждении почты
    # переводить его в состояние "is.active=True". Ниже я закомментил этот
    # вариант реализации.
    user.password = default_token_generator.make_token(user)
    # TODO: при принятии этого решения - надо переделать регистрацию,
    #       либо переделать поле модели (что надежнее)
    #       is_active = models.BooleanField(default=False)
    # user.is_active = True
    user.save()
    send_mail(
        subject=EMAIL_CONFIRM_SUBJECT,
        message=EMAIL_CONFIRM_TEXT.format(
            username=user.username,
            password=user.password
        ),
        to=(user.email,)
    )
    return Response(
        data="Email has confirmed! Please check you mailbox",
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def order_create(request):
    """Создать заказ."""
    serializer = PostOrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(request.data, status=status.HTTP_201_CREATED)


class OrderViewSet(viewsets.ModelViewSet):
    """Список заказов."""
    permission_classes = [permissions.AllowAny, ]
    queryset = Order.objects.all()
    methods=['get', 'post', 'patch', 'delete'],
    serializer_class = GetOrderSerializer

    def perform_update(self, serializer):
        serializer.save()

    @action(
        detail=True,
        methods=['patch', ],
        permission_classes=(permissions.IsAuthenticated, IsOwner)
    )
    def pay(self, request, pk):
        """Оплатить заказ."""
        order = get_object_or_404(Order, id=pk)
        serializer = PaySerializer(order, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['patch', ],
        permission_classes=(permissions.IsAuthenticated, IsOwner)
    )
    def cancell(self, request, pk):
        """Отменить заказ."""
        order = get_object_or_404(Order, id=pk)
        serializer = CancellSerializer(order, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['patch', ],
        permission_classes=(permissions.IsAuthenticated, IsOwner)
    )
    def comment(self, request, pk):
        """Добавить комментарий к заказу."""
        order = get_object_or_404(Order, id=pk)
        serializer = CommentSerializer(order, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(
        detail=True,
        methods=['patch', ],
        permission_classes=(permissions.IsAuthenticated, IsOwner)
    )
    def change_datetime(self, request, pk):
        """Перенести заказ."""
        order = get_object_or_404(Order, id=pk)
        serializer = DateTimeSerializer(order, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(
        detail=True,
        methods=['patch', ],
        permission_classes=(permissions.IsAdminUser,)
    )
    def change_status(self, request, pk):
        """Изменить статус заказа."""
        order = get_object_or_404(Order, id=pk)
        serializer = OrderStatusSerializer(order, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class RatingViewSet(viewsets.ModelViewSet):
    """Список отзывов."""
    queryset = Rating.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = RatingSerializer
    methods=['get', 'post', 'patch', 'delete'],


    def perform_create(self, serializer):
        order_id = self.kwargs.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        serializer.save(user=self.request.user, order=order)
