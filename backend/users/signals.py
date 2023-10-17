"""
Перечень Django-signals приложения Users.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver


from api.utils import send_mail
from cleanpro.app_data import EMAIL_REGISTER_SUBJECT, EMAIL_REGISTER_TEXT
from users.models import User


def sent_register_email(user: User):
    """
    Посылает электронное письмо с подтверждением регистрации пользователя.
    """
    send_mail(
        subject=EMAIL_REGISTER_SUBJECT,
        message=EMAIL_REGISTER_TEXT,
        to=(user.email,),
    )
    return


@receiver(signal=post_save, sender=User)
def post_save_receiver(sender, instance, created, **kwargs):
    """
    Получает сигнал post_save и направляет на соответствующий обработчик.
    """
    if isinstance(instance, User):
        sent_register_email(user=instance)
    return
