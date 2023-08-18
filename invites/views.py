from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from .models import Invitation
from communities.models import Community
from .serializers import InvitationSerializer

class UserCommunityView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_communities = request.user.joined_communities.all()
        community_names = [community.name for community in user_communities]
        return Response({'user_communities': community_names}, status=status.HTTP_200_OK)

class InvitationViewSet(ModelViewSet):
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['POST'])
    def send_invite(self, request):
        try:
            community_id = request.data.get('community_id')
            invitee_username = request.data.get('invitee_username')
            community = Community.objects.get(id=community_id)
            invitee = User.objects.get(username=invitee_username)
            
            if community.members.filter(pk=invitee.pk).exists():
                return Response({'detail': 'User is already a member of this community.'}, status=status.HTTP_400_BAD_REQUEST)
            
            if Invitation.objects.filter(community=community, invitee=invitee).exists():
                return Response({'detail': 'An invitation to this user for this community already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            
            Invitation.objects.create(inviter=request.user, community=community, invitee=invitee)
            return Response({'detail': 'Invitation sent successfully.'}, status=status.HTTP_201_CREATED)
        except (Community.DoesNotExist, User.DoesNotExist):
            return Response({'detail': 'Invalid community or invitee username.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'])
    def accept_invite(self, request, pk=None):
        try:
            invitation = self.get_object()
            if invitation.invitee != request.user or invitation.accepted:
                return Response({'detail': 'Invitation not found or already accepted.'}, status=status.HTTP_404_NOT_FOUND)
            
            community = invitation.community
            community.members.add(request.user)
            
            invitation.accepted = True
            invitation.save()
            
            return Response({'detail': 'Invitation accepted and user added to community.'}, status=status.HTTP_200_OK)
        except Invitation.DoesNotExist:
            return Response({'detail': 'Invitation not found or already accepted.'}, status=status.HTTP_404_NOT_FOUND)
