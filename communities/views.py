from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Community
from .serializers import CommunitySerializer
from web_3_degenz.permissions import IsOwnerOrReadOnly, IsCommunityMember
from django.contrib.auth.models import User
from posts.models import Post
from posts.serializers import PostSerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action


class CommunityList(generics.ListCreateAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommunityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.owner != request.user:
            return Response({'detail': 'You are not the owner of this community.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def update_moderators(self, request, pk=None):
        community = self.get_object()

        if community.owner != self.request.user:
            return Response({'detail': 'You are not the owner of this community.'}, status=status.HTTP_403_FORBIDDEN)

        moderators_to_add = request.data.get('moderators_to_add', [])
        moderators_to_remove = request.data.get('moderators_to_remove', [])

        if not all(isinstance(moderator_id, int) for moderator_id in moderators_to_add + moderators_to_remove):
            return Response({'detail': 'Invalid moderator IDs.'}, status=status.HTTP_400_BAD_REQUEST)

        moderators_to_add_users = User.objects.filter(id__in=moderators_to_add)
        community.moderators.add(*moderators_to_add_users)

        moderators_to_remove_users = User.objects.filter(id__in=moderators_to_remove)
        community.moderators.remove(*moderators_to_remove_users)

        community.save()

        active_moderators = community.moderators.all()

        serializer = CommunitySerializer(community, context={'request': request})
        return Response({'detail': 'Moderators updated successfully.', 'active_moderators': active_moderators}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def update_members(self, request, pk=None):
        community = self.get_object()

        if community.owner != self.request.user:
            return Response({'detail': 'You are not the owner of this community.'}, status=status.HTTP_403_FORBIDDEN)

        members_to_remove = request.data.get('members_to_remove', [])

        if not all(isinstance(member_id, int) for member_id in members_to_remove):
            return Response({'detail': 'Invalid member IDs.'}, status=status.HTTP_400_BAD_REQUEST)

        members_to_remove_users = User.objects.filter(id__in=members_to_remove)
        community.members.remove(*members_to_remove_users)

        community.save()

        serializer = CommunitySerializer(community, context={'request': request})
        return Response({'detail': 'Members removed successfully.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def add_moderators(self, request, pk=None):
        community = self.get_object()

        if community.owner != self.request.user:
            return Response({'detail': 'You are not the owner of this community.'}, status=status.HTTP_403_FORBIDDEN)

        moderators_to_add = request.data.get('moderators_to_add', [])

        if not all(isinstance(moderator_id, int) for moderator_id in moderators_to_add):
            return Response({'detail': 'Invalid moderator IDs.'}, status=status.HTTP_400_BAD_REQUEST)

        moderators_to_add_users = User.objects.filter(id__in=moderators_to_add)
        community.moderators.add(*moderators_to_add_users)

        community.save()

        serializer = CommunitySerializer(community, context={'request': request})
        return Response({'detail': 'Moderators added successfully.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def remove_moderators(self, request, pk=None):
        community = self.get_object()

        if community.owner != self.request.user:
            return Response({'detail': 'You are not the owner of this community.'}, status=status.HTTP_403_FORBIDDEN)

        moderators_to_remove = request.data.get('moderators_to_remove', [])

        if not all(isinstance(moderator_id, int) for moderator_id in moderators_to_remove):
            return Response({'detail': 'Invalid moderator IDs.'}, status=status.HTTP_400_BAD_REQUEST)

        moderators_to_remove_users = User.objects.filter(id__in=moderators_to_remove)
        community.moderators.remove(*moderators_to_remove_users)

        community.save()

        serializer = CommunitySerializer(community, context={'request': request})
        return Response({'detail': 'Moderators removed successfully.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def remove_post(self, request, pk=None):
        community = self.get_object()

        if community.owner != self.request.user and not community.moderators.filter(pk=self.request.user.pk).exists():
            return Response({'detail': 'You do not have permission to remove posts in this community.'}, status=status.HTTP_403_FORBIDDEN)
        
        post_id_to_remove = request.data.get('post_id')
        if post_id_to_remove:
            try:
                post_to_remove = Post.objects.get(id=post_id_to_remove)
                if community.owner == self.request.user or community.moderators.filter(pk=self.request.user.pk).exists():
                    post_to_remove.delete()
                    return Response({'detail': 'Post removed successfully.'}, status=status.HTTP_200_OK)
                else:
                    return Response({'detail': 'You do not have permission to remove this post.'}, status=status.HTTP_403_FORBIDDEN)
            except Post.DoesNotExist:
                return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)
            except:
                return Response({'detail': 'An error occurred while trying to remove the post.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'detail': 'Invalid post ID provided.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def remove_member(self, request, pk=None):
        community = self.get_object()

        if community.owner != self.request.user and not community.moderators.filter(pk=self.request.user.pk).exists():
            return Response({'detail': 'You do not have permission to remove members from this community.'}, status=status.HTTP_403_FORBIDDEN)

        members_to_remove = request.data.get('members_to_remove', [])

        if not all(isinstance(member_id, int) for member_id in members_to_remove):
            return Response({'detail': 'Invalid member IDs.'}, status=status.HTTP_400_BAD_REQUEST)

        members_to_remove_users = User.objects.filter(id__in=members_to_remove)
        community.members.remove(*members_to_remove_users)

        community.save()

        return Response({'detail': 'Members removed successfully.'}, status=status.HTTP_200_OK)


class CommunityPostList(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsCommunityMember]

    def get_queryset(self):
        community_id = self.kwargs.get('pk')
        community = get_object_or_404(Community, id=community_id)

        if community.privacy == 'public' or self.request.user in community.members.all():
            return Post.objects.filter(community=community)
        else:
            return Post.objects.none()

    def perform_create(self, serializer):
        community_id = self.kwargs.get('pk')
        community = get_object_or_404(Community, id=community_id)
        serializer.save(owner=self.request.user, community=community)
