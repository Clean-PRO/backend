from django.apps import AppConfig
from django.db.models.signals import post_save


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = 'Пользователи'

    def ready(self) -> None:
        from .signals import post_save_receiver

        post_save.connect(
            receiver=post_save_receiver,
            dispatch_uid='update_cached_reviews',
        )
        return super().ready()
