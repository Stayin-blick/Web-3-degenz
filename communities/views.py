from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Community, CommunityPost
from .serializers import CommunitySerializer, CommunityPostSerializer, CommunityEditSerializer
from web_3_degenz.permissions import IsCommunityOwnerOrModerator, IsPostOwner, IsCommunityMember
import humanize

class CommunityListCreateView(generics.ListCreateAPIView):
    serializer_class = CommunitySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        user_communities = Community.objects.filter(members=user)
        public_communities = Community.objects.filter(privacy='public')
        private_communities = Community.objects.filter(privacy='private')
        user_communities.update(last_visited=timezone.now())
        
        queryset = (user_communities | public_communities | private_communities).distinct().order_by('-last_visited')

        for community in queryset:
            community.last_visited = humanize.naturaltime(community.last_visited)

        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CommunityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [IsCommunityOwnerOrModerator]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Store the previous members and moderator
        previous_members = list(instance.members.all())
        previous_moderator = instance.moderators.first()  # Get the previous moderator

        self.perform_update(serializer)

        # Get the new members and moderator
        new_members = list(instance.members.exclude(id__in=[user.id for user in previous_members]))
        new_moderator = instance.moderators.first()  # Get the new moderator

        response_data = serializer.data

        # Include the current members and moderator in the response
        current_members = [f'user:{member.username}' for member in instance.members.all()]
        current_moderator = f'user:{previous_moderator.username}' if previous_moderator else None

        # Modify the response to include the added member and moderator
        response_data['message'] = {
            'current_members': current_members,
            'current_moderator': current_moderator,
            'added_members': [f'user:{member.username}' for member in new_members],
            'added_moderator': f'user:{new_moderator.username}' if new_moderator else None,
            'removed_members': [],
            'removed_moderator': f'user:{previous_moderator.username}' if previous_moderator else None
        }

        return Response(response_data)

    def perform_update(self, serializer):
        instance = serializer.save()

        # Ensure only community members can be moderators
        new_moderator = instance.moderators.first()
        if new_moderator and new_moderator not in instance.members.all():
            instance.moderators.remove(new_moderator)

        instance.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Ensure only the community owner can delete the community
        if request.user != instance.owner:
            return Response({'detail': 'You do not have permission to delete this community.'}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()

        # Ensure only the community owner, moderators, or post owner can delete the post
        if not (
            request.user == instance.owner
            or request.user in instance.moderators.all()
        ):
            return Response({'detail': 'You do not have permission to delete this community.'}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def remove_member(self, request, *args, **kwargs):
        community = self.get_object()

        # Ensure only the community owner or moderators can remove members
        if not (
            request.user == community.owner
            or request.user in community.moderators.all()
        ):
            return Response({'detail': 'You do not have permission to remove members from this community.'}, status=status.HTTP_403_FORBIDDEN)

        username = request.data.get('username', None)
        if not username:
            return Response({'detail': 'Please provide a username to remove from the community.'}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, username=username)
        
        # Ensure the user is a member of the community
        if user not in community.members.all():
            return Response({'detail': 'The specified user is not a member of this community.'}, status=status.HTTP_400_BAD_REQUEST)

        # Remove the user from the community
        community.members.remove(user)
        community.save()

        return Response({'detail': f'The user {username} has been removed from the community.'}, status=status.HTTP_200_OK)

class CommunityInfoView(generics.RetrieveAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [permissions.IsAuthenticated] 

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        return Response(data)

class CommunityPostListCreateView(generics.ListCreateAPIView):
    queryset = CommunityPost.objects.all()
    serializer_class = CommunityPostSerializer
    permission_classes = [permissions.IsAuthenticated, IsCommunityMember]
    
class CommunityPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CommunityPost.objects.all()
    serializer_class = CommunityPostSerializer

class UserPostDeleteView(generics.DestroyAPIView):
    queryset = CommunityPost.objects.all()
    serializer_class = CommunityPostSerializer
    permission_classes = [permissions.IsAuthenticated, IsPostOwner]

    def perform_destroy(self, instance):
        instance.delete()

class CommunityEditView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunityEditSerializer
    permission_classes = [IsCommunityOwnerOrModerator]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # Store the previous members and moderator
        previous_members = list(instance.members.all())
        previous_moderator = instance.moderators.first()

        self.perform_update(serializer)

        # Get the new members and moderator
        new_members = list(instance.members.exclude(id__in=[user.id for user in previous_members]))
        new_moderator = instance.moderators.first()

        response_data = serializer.data

        # Include the current members and moderator in the response
        current_members = [f'user:{member.username}' for member in instance.members.all()]
        current_moderator = f'user:{previous_moderator.username}' if previous_moderator else None

        # Modify the response to include the added member and moderator
        response_data['message'] = {
            'current_members': current_members,
            'current_moderator': current_moderator,
            'added_members': [f'user:{member.username}' for member in new_members],
            'added_moderator': f'user:{new_moderator.username}' if new_moderator else None,
            'removed_members': [],
            'removed_moderator': f'user:{previous_moderator.username}' if previous_moderator else None
        }

        return Response(response_data)

    def perform_update(self, serializer):
        instance = serializer.save()

        # Ensure only community members can be moderators
        new_moderator = instance.moderators.first()
        if new_moderator and new_moderator not in instance.members.all():
            instance.moderators.remove(new_moderator)

        instance.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Ensure only the community owner can delete the community
        if request.user != instance.owner:
            return Response({'detail': 'You do not have permission to delete this community.'}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()

        # Ensure only the post owner, community owner, or moderators can delete the post
        if not (
            request.user == instance.owner
            or request.user == instance.community.owner
            or request.user in instance.community.moderators.all()
        ):
            return Response({'detail': 'You do not have permission to delete this post.'}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def remove_member(self, request, *args, **kwargs):
        community = self.get_object()

        # Ensure only the community owner or moderators can remove members
        if not (
            request.user == community.owner
            or request.user in community.moderators.all()
        ):
            return Response({'detail': 'You do not have permission to remove members from this community.'}, status=status.HTTP_403_FORBIDDEN)

        username = request.data.get('username', None)
        if not username:
            return Response({'detail': 'Please provide a username to remove from the community.'}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, username=username)
        
        # Ensure the user is a member of the community
        if user not in community.members.all():
            return Response({'detail': 'The specified user is not a member of this community.'}, status=status.HTTP_400_BAD_REQUEST)

        # Remove the user from the community
        community.members.remove(user)
        community.save()

        return Response({'detail': f'The user {username} has been removed from the community.'}, status=status.HTTP_200_OK)