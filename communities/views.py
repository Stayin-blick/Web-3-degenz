from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Community
from .serializers import CommunitySerializer
from web_3_degenz.permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User  


class CommunityList(generics.ListCreateAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CommunityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def invite_user(self, request, pk=None):
        community = self.get_object()
        invitee_username = request.data.get('invitee_username')
        invitee = User.objects.get(username=invitee_username)
        
        if community.members.filter(pk=invitee.pk).exists():
            return Response({'detail': 'User is already a member of this community.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if Invitation.objects.filter(inviter=request.user, community=community, invitee=invitee).exists():
            return Response({'detail': 'Invitation already sent to this user.'}, status=status.HTTP_400_BAD_REQUEST)
        
        Invitation.objects.create(inviter=request.user, community=community, invitee=invitee)
        return Response({'detail': 'Invitation sent successfully.'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put'])
    def edit_community(self, request, pk=None):
        community = self.get_object()

        if community.owner != self.request.user:
            return Response({'detail': 'You are not the owner of this community.'}, status=status.HTTP_403_FORBIDDEN)

        name = request.data.get('name')
        if name:
            community.name = name

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
        return Response({'detail': 'Community details updated successfully.', 'active_moderators': active_moderators}, status=status.HTTP_200_OK)
