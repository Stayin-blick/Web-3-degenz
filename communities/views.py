from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Community
from .serializers import CommunitySerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class CommunityList(generics.ListCreateAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [IsAuthenticated]

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
            return Response({'detail': 'User is already a member of this community.'}, status=400)
        
        if Invitation.objects.filter(inviter=request.user, community=community, invitee=invitee).exists():
            return Response({'detail': 'Invitation already sent to this user.'}, status=400)
        
        invitation = Invitation.objects.create(inviter=request.user, community=community, invitee=invitee)
        return Response({'detail': 'Invitation sent successfully.'}, status=201)

    @action(detail=True, methods=['put'])
    def edit_community(self, request, pk=None):
        community = self.get_object()

        if community.owner != self.request.user:
            return Response({'detail': 'You are not the owner of this community.'}, status=403)

        name = request.data.get('name')
        if name:
            community.name = name

        moderators_to_add = request.data.get('moderators_to_add', [])
        moderators_to_remove = request.data.get('moderators_to_remove', [])

        for moderator_id in moderators_to_add:
            moderator = User.objects.get(id=moderator_id)
            community.moderators.add(moderator)

        for moderator_id in moderators_to_remove:
            moderator = User.objects.get(id=moderator_id)
            community.moderators.remove(moderator)

        community.save()

        return Response({'detail': 'Community details updated successfully.'}, status=200)
