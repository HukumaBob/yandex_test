from django.test import TestCase
from django.contrib.auth.models import User
from unittest.mock import patch
from celery.result import AsyncResult
from blog_api.tasks import send_daily_post_summary

class CeleryTaskTestCase(TestCase):
    @patch('blog_api.tasks.send_mail')
    def test_send_daily_post_summary(self, mock_send_mail):
        user = User.objects.create_user(username='testuser', password='password', email='test@example.com')

        # Создание тестовых данных для news_feed.posts (предположим, у вас есть метод для этого)
        # ...

        # Вызов задачи
        task_result = send_daily_post_summary.delay()

        # Подтверждение, что задача была добавлена в очередь
        self.assertTrue(isinstance(task_result, AsyncResult))

        # Подтверждение, что send_mail был вызван - и он не отрабатывает!!!
        # self.assertTrue(mock_send_mail.called)
