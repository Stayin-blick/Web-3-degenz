from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from invites.models import Invitation
from .models import Community
from django.contrib.auth.models import User

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_invite(request):
    try:
        community_id = request.data.get('community_id')
        invitee_username = request.data.get('invitee_username')
        community = Community.objects.get(id=community_id)
        invitee = User.objects.get(username=invitee_username)
        
        if community.members.filter(pk=invitee.pk).exists():
            return Response({'detail': 'User is already a member of this community.'}, status=400)
        
        if Invitation.objects.filter(community=community, invitee=invitee).exists():
            return Response({'detail': 'An invitation to this user for this community already exists.'}, status=400)
        
        Invitation.objects.create(inviter=request.user, community=community, invitee=invitee)
        return Response({'detail': 'Invitation sent successfully.'}, status=201)
    except (Community.DoesNotExist, User.DoesNotExist):
        return Response({'detail': 'Invalid community or invitee username.'}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_invite(request, invitation_id):
    try:
        invitation = Invitation.objects.get(id=invitation_id, invitee=request.user, accepted=False)
        community = invitation.community
    except Invitation.DoesNotExist:
        return Response({'detail': 'Invitation not found or already accepted.'}, status=404)
    
    community.members.add(request.user)
    
    invitation.accepted = True
    invitation.save()
    
    return Response({'detail': 'Invitation accepted and user added to community.'}, status=200)

