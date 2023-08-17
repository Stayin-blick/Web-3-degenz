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
