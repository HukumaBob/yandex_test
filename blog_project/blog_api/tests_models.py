from django.test import TestCase
from .models import Blog, Post, Subscription, NewsFeed
from django.contrib.auth.models import User

class ModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.blog = Blog.objects.create(owner=self.user)
        self.post = Post.objects.create(blog=self.blog, title='Test Post', text='This is a test post')

    def test_blog_creation(self):
        self.assertEqual(self.blog.owner, self.user)

    def test_post_creation(self):
        self.assertEqual(self.post.blog, self.blog)

    def test_subscription_creation(self):
        subscription = Subscription.objects.create(subscriber=self.user, blog=self.blog)
        self.assertEqual(subscription.subscriber, self.user)

    def test_news_feed_creation(self):
        news_feed = NewsFeed.objects.create(user=self.user)
        self.assertEqual(news_feed.user, self.user)
