from django.db.models import Count
from rest_framework import generics, permissions, filters
from web_3_degenz.permissions import IsOwnerOrReadOnly, IsCommunityMember
from .models import Post
from .serializers import PostSerializer
from django_filters.rest_framework import DjangoFilterBackend
from communities.models import Community
from django.shortcuts import get_object_or_404


class PostList(generics.ListCreateAPIView):
    """
    List posts or create a post if logged in
    The perform_create method associates the post with the logged in user.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.annotate(
        likes_count = Count('likes', distinct=True),
        comments_count = Count('comment', distinct=True)
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    ordering_fields = [
        'likes_count', 
        'comments_count', 
        'likes__created_at',
    ]
    search_fields = [
        'owner__username', 'title'
    ]
    filterset_fields = [
        'owner__profile', 
        'owner__followed__owner__profile', 
        'likes__owner__profile'
    ]

    def perform_create(self, serializer):
        community_id = self.request.data.get('community')
        if community_id:
            community = get_object_or_404(Community, id=community_id)
            serializer.save(owner=self.request.user, community=community)
        else:
            serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a post and edit or delete it if you own it.
    """
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comment', distinct=True)
    ).order_by('-created_at')


class CommunityPostList(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsCommunityMember]

    def get_queryset(self):
        community_id = self.kwargs['community_id']
        community = get_object_or_404(Community, id=community_id)
        return Post.objects.filter(community=community)


class CommunityPostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a post and edit or delete it if you own it.
    """
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comment', distinct=True)
    ).order_by('-created_at')
