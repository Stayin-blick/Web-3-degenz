from django.db.models import Count
from rest_framework import generics, permissions, filters
from web_3_degenz.permissions import IsOwnerOrReadOnly
from .models import Post
from .serializers import PostSerializer
from django_filters.rest_framework import DjangoFilterBackend


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
        'likes_count', 'comments_count', 'likes__created_at',
    ]
    search_fields = [
        'owner__username', 'title'
    ]
    filterset_fields = [
        'owner__profile', 'owner__followed__owner__profile', 'likes__owner__profile'
    ]

    def perform_create(self, serializer):
        community_id = self.request.data.get('community')  
        if community_id:
            community = Community.objects.get(id=community_id)
            serializer.save(owner=self.request.user, community=community)
        else:
            serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a post and edit or delete it if you own it.
    """
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.all()
