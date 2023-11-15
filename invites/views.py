from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Invitation
from communities.models import Community
from .serializers import InvitationListSerializer, InvitationAcceptSerializer, InvitationSendSerializer
from web_3_degenz.permissions import IsCommunityMember

class InvitationListView(generics.ListAPIView):
    serializer_class = InvitationListSerializer
    permission_classes = [permissions.IsAuthenticated, IsCommunityMember]

    def get_queryset(self):
        user = self.request.user
        return Invitation.objects.filter(invitee=user, accepted=False)

class InvitationCreateView(generics.CreateAPIView):
    serializer_class = InvitationSendSerializer
    permission_classes = [permissions.IsAuthenticated, IsCommunityMember]

    def get_queryset(self):
        return Community.objects.filter(members=self.request.user)

    def perform_create(self, serializer):
        serializer.save(inviter=self.request.user)

class InvitationAcceptView(generics.UpdateAPIView):
    serializer_class = InvitationAcceptSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Invitation.objects.filter(invitee=user, accepted=False)

    def perform_update(self, serializer):
        invitation = serializer.instance

        # Check if the invitation has already been accepted
        if invitation.accepted:
            raise serializers.ValidationError("This invitation has already been accepted.")

        # Check if the user accepting the invitation is the same as the invitee
        if invitation.invitee != self.request.user:
            raise serializers.ValidationError("You are not authorized to accept this invitation.")

        community = invitation.community

        # Check if the user is already a member of the community
        if community.members.filter(username=self.request.user.username).exists():
            raise serializers.ValidationError("You are already a member of this community.")

        # Update the community membership and set the invitation as accepted
        community.members.add(self.request.user)
        invitation.accepted = True
        invitation.save()
