from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogViewSet, PostViewSet, SubscriptionViewSet

router = DefaultRouter()
router.register(r'blogs', BlogViewSet)
router.register(r'posts', PostViewSet)
router.register(r'subscriptions', SubscriptionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
