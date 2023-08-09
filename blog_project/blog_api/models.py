from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User


class Blog(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.owner.username


class Post(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Subscription(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE, related_name='subscribers')
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.subscriber == self.blog.owner:
            raise ValidationError("You cannot subscribe to your own blog.")

    def __str__(self):
        return f'{self.subscriber} subscribe to {self.blog.owner}'

    class Meta:
        unique_together = ['subscriber', 'blog']


class NewsFeed(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='news_feed')
    posts = models.ManyToManyField(Post, related_name='news_feeds')

    def __str__(self):
        return f'News feed of {self.user}'
