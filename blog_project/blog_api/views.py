from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Blog, Post, Subscription
from .serializers import BlogSerializer, PostSerializer, SubscriptionSerializer


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    @action(detail=True, methods=['post'])
    def subscribe(self, request, pk=None):
        blog = self.get_object()
        subscriber = request.user

        if not blog.subscribers.filter(subscriber=subscriber).exists():
            Subscription.objects.create(subscriber=subscriber, blog=blog)
            return Response({'detail': 'Subscribed successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'Already subscribed'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def unsubscribe(self, request, pk=None):
        blog = self.get_object()
        subscriber = request.user

        if blog.subscribers.filter(subscriber=subscriber).exists():
            blog.subscribers.filter(subscriber=subscriber).delete()
            return Response({'detail': 'Unsubscribed successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Not subscribed'}, status=status.HTTP_400_BAD_REQUEST)
