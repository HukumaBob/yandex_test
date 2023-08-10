from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Blog, Post


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.blog = Blog.objects.create(owner=self.user)
        self.post = Post.objects.create(blog=self.blog, title='Test Post', text='This is a test post')

    def test_create_post(self):
        url = reverse('post-list')
        data = {'blog': self.blog.id, 'title': 'New Post', 'text': 'This is a new post'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_mark_post_as_read(self):
        url = reverse('mark_post_as_read', kwargs={'post_id': self.post.id})
        response = self.client.patch(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
