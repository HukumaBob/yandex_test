from rest_framework import viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Blog, Post, Subscription, NewsFeed
from .serializers import BlogSerializer, PostSerializer, SubscriptionSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer


class UserRegistration(APIView):
    """
    API endpoint for user registration. Creates a new user and associates a news feed with them.
    """

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            NewsFeed.objects.create(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogViewSet(viewsets.ModelViewSet):
    """
    API endpoint for CRUD operations on blogs.
    """

    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint for CRUD operations on posts. Also handles post creation and news feed updates.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        post = serializer.save()

        subscribers = post.blog.subscribers.all()
        for subscriber in subscribers:
            subscriber.news_feed.posts.add(post)

        user = post.blog.owner
        news_feed = user.news_feed
        if news_feed.posts.count() > 500:
            extra_posts = news_feed.posts.all().order_by('created_at')[:news_feed.posts.count() - 500]
            news_feed.posts.remove(*extra_posts)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_post_as_read(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if post.blog.owner != request.user:  # User can to mark only his own posts
        return Response(status=status.HTTP_403_FORBIDDEN)

    post.read = True
    post.save()
    return Response(status=status.HTTP_200_OK)


class SubscriptionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for CRUD operations on subscriptions. Provides additional actions for subscribing
    and unsubscribing from blogs.
    """

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    @action(detail=True, methods=['post'])
    def subscribe(self, request, pk=None):
        """
        Subscribe to a blog.
        """
        blog = self.get_object()
        subscriber = request.user

        if not blog.subscribers.filter(subscriber=subscriber).exists():
            Subscription.objects.create(subscriber=subscriber, blog=blog)
            return Response({'detail': 'Subscribed successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'Already subscribed'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def unsubscribe(self, request, pk=None):
        """
        Unsubscribe from a blog.
        """
        blog = self.get_object()
        subscriber = request.user

        if blog.subscribers.filter(subscriber=subscriber).exists():
            blog.subscribers.filter(subscriber=subscriber).delete()
            return Response({'detail': 'Unsubscribed successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Not subscribed'}, status=status.HTTP_400_BAD_REQUEST)


class NewsFeedViewSet(viewsets.GenericViewSet):
    """
    API endpoint for retrieving the personal news feed of the authenticated user.
    """

    serializer_class = PostSerializer

    @action(detail=False, methods=['get'])
    def personal_feed(self, request):
        """
        Retrieve the personal news feed of the authenticated user.
        """
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
