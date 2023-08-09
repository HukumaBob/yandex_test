from django.contrib import admin
from .models import Blog, Post, Subscription, NewsFeed

admin.site.register(Blog)
admin.site.register(Post)
admin.site.register(Subscription)
admin.site.register(NewsFeed)
