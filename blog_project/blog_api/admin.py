from django.contrib import admin
from .models import Blog, Post, Subscription

admin.site.register(Blog)
admin.site.register(Post)
admin.site.register(Subscription)
