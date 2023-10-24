from rest_framework import permissions


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

    def has_object_permission(self, request, view, obj):
        # TODO: данная проверка дублирует логику has_permission,
        #       а также не имеет отношения к объекту.
        return request.user.is_staff


# TODO: я понял, что мне тут не понравилось исходно,
#       когда на ревью написали "Не понимаю назначение этого класса".
#       Проверка "не администратор" представляет собой проверку "владелец".
#       В контексте использования: оплатить заказ может только владелец заказа.
class IsNotAdmin(permissions.BasePermission):
    """
    Запрещает доступ администратору.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            not request.user.is_staff
        )


class IsOwner(permissions.BasePermission):
    """
    Предоставляет доступ:
        - на чтение: авторизированному пользователю
        - на запись: только администратору и автору
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # TODO: данная проверка второй частью дублирует логику has_permission,
        #       а также не имеет отношения к объекту.
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
        # TODO: данная проверка второй частью должна быть в has_permission,
        #       а также не имеет отношения к объекту.
        return request.user == obj.user or request.user.is_staff
