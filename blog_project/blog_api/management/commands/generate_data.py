from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from mixer.backend.django import mixer

# Импортируй модели
from blog_api.models import Blog, Post


class Command(BaseCommand):
    help = 'Generate test data'

    def handle(self, *args, **options):
        # Генерация пользователей
        for _ in range(1000):  # Создай 1000 пользователей
            mixer.blend(User)

        # Генерация блогов
        users = User.objects.all()
        for user in users:
            mixer.blend(Blog, owner=user)

        # Генерация постов
        blogs = Blog.objects.all()
        for _ in range(5000):  # Создай 5000 постов
            blog = mixer.blend(Blog)
            mixer.blend(Post, blog=blog)

        self.stdout.write(self.style.SUCCESS('Data generation complete.'))
