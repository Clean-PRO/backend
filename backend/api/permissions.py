from rest_framework import permissions

from cleanpro.app_data import ORDER_CREATED_STATUS


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Предоставляет доступ:
        - на чтение: всем
        - на запись: только администратору
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or
            request.user.is_staff
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Предоставляет доступ:
        - на чтение: авторизированному пользователю
        - на запись: только администратору и автору
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user or request.user.is_staff


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Предоставляет доступ:
        - на чтение: всем
        - на запись: автору объекта или администратору
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user or request.user.is_staff


class IsOwnerAbleToPay(permissions.BasePermission):
    """
    Предоставляет доступ для оплаты заказа:
        - только автору объекта
        - только по методу POST
        - только если заказ имеет статус "создан"
    """

    def has_permission(self, request, view):
        return (
            request.method == 'POST' and
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user == obj.user and
            obj.order_status == ORDER_CREATED_STATUS
        )
