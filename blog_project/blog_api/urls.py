from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (BlogViewSet,
                    PostViewSet,
                    SubscriptionViewSet,
                    NewsFeedViewSet,
                    mark_post_as_read,
                    )

router = DefaultRouter()
router.register(r'blogs', BlogViewSet)
router.register(r'posts', PostViewSet)
router.register(r'subscriptions', SubscriptionViewSet)
router.register(r'news-feed', NewsFeedViewSet, basename='news-feed')

urlpatterns = [
    path(
        'posts/<int:post_id>/mark_as_read/',
        mark_post_as_read,
        name='mark_post_as_read'
    ),
    path('', include(router.urls)),
]
