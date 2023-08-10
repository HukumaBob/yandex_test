from django.conf import settings
from django.contrib.auth.models import User
from celery import shared_task
from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_daily_post_summary():
    logger.info('Sending daily post summary email...')
    users = User.objects.all()

    for user in users:
        news_feed = user.news_feed
        recent_posts = news_feed.posts.all().order_by('-created_at')[:5]

        subject = 'Daily Post Summary'
        message = '\n'.join([f'{post.title}: {post.text}' for post in recent_posts])
        from_email = settings.EMAIL_ADMIN
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
