from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (BlogViewSet,
                    PostViewSet,
                    SubscriptionViewSet,
                    NewsFeedViewSet,
                    )

router = DefaultRouter()
router.register(r'blogs', BlogViewSet)
router.register(r'posts', PostViewSet)
router.register(r'subscriptions', SubscriptionViewSet)
router.register(r'news-feed', NewsFeedViewSet, basename='news-feed')

urlpatterns = [
    path('', include(router.urls)),
]
