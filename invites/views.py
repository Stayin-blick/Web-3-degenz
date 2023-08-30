from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Invitation
from communities.models import Community
from .serializers import InvitationSerializer
from web_3_degenz.permissions import IsCommunityMember

class InvitationListView(generics.ListAPIView):
    serializer_class = InvitationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Invitation.objects.filter(invitee=user, accepted=False)

class InvitationCreateView(generics.CreateAPIView):
    serializer_class = InvitationSerializer
    permission_classes = [permissions.IsAuthenticated, IsCommunityMember]

    def get_queryset(self):
        return Community.objects.filter(members=self.request.user)

    def perform_create(self, serializer):
        inviter = self.request.user
        community = serializer.validated_data['community']
        invitee_username = serializer.validated_data['invitee_username']

        # Check if the invitee is already a member of the community
        if community.members.filter(username=invitee_username).exists():
            raise serializers.ValidationError("The user is already a member of the community.")

        # Check if an invitation from the same inviter to the same community for the same invitee exists
        if Invitation.objects.filter(inviter=inviter, community=community, invitee__username=invitee_username).exists():
            raise serializers.ValidationError("You have already invited this user to the community.")

        serializer.save(inviter=inviter)

class InvitationAcceptView(generics.UpdateAPIView):
    serializer_class = InvitationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Invitation.objects.filter(invitee=user, accepted=False)

    def perform_update(self, serializer):
        invitation = serializer.instance
        community = invitation.community
        community.members.add(invitation.invitee)
        invitation.accepted = True
        invitation.save()