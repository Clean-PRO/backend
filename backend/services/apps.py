from django.apps import AppConfig
from django.db.models.signals import post_save


class ServiceConfig(AppConfig):
    name = 'services'
    verbose_name = 'Услуги'

    def ready(self) -> None:
        from services.signals import post_save_receiver

        post_save.connect(
            receiver=post_save_receiver,
            dispatch_uid='update_cached_reviews',
        )

        return super().ready()
