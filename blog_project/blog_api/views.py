from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Blog, Post, Subscription, NewsFeed
from .serializers import BlogSerializer, PostSerializer, SubscriptionSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer


class UserRegistration(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            NewsFeed.objects.create(user=user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        post = serializer.save()

        # Добавление поста в ленту новостей подписчиков блога
        subscribers = post.blog.subscribers.all()
        for subscriber in subscribers:
            subscriber.news_feed.posts.add(post)

        # Ограничение количества постов в ленте новостей до 500
        user = post.blog.owner
        news_feed = user.news_feed
        if news_feed.posts.count() > 500:
            extra_posts = news_feed.posts.all().order_by('created_at')[:news_feed.posts.count() - 500]
            news_feed.posts.remove(*extra_posts)


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


class NewsFeedViewSet(viewsets.GenericViewSet):
    serializer_class = PostSerializer

    @action(detail=False, methods=['get'])
    def personal_feed(self, request):
        user = request.user
        posts = user.news_feed.posts.all().order_by('-created_at')

        if posts.count() > 500:
            posts = posts[:500]

        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
