from django.contrib.auth.models import User
from celery import Celery, shared_task
from celery.schedules import crontab
from django.core.mail import send_mail

app = Celery('blog_api')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    # ...
    'send_daily_post_summary': {
        'task': 'blog_api.tasks.send_daily_post_summary',
        'schedule': crontab(minute=0, hour=1),  # Every midnight
    },
}


@shared_task
def send_daily_post_summary():
    users = User.objects.all()

    for user in users:
        news_feed = user.news_feed
        recent_posts = news_feed.posts.all().order_by('-created_at')[:5]

        subject = 'Daily Post Summary'
        message = '\n'.join([f'{post.title}: {post.text}' for post in recent_posts])
        from_email = 'your_email@example.com'
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=True)
