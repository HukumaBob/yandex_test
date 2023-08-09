from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogViewSet, PostViewSet

router = DefaultRouter()
router.register(r'blogs', BlogViewSet)
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
]