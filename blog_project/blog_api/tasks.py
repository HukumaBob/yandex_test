from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_daily_email():
    pass
    # Ваш код для формирования и отправки ежедневной подборки постов на почту
