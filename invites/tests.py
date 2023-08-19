from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from rest_framework.decorators import action
from .models import Invitation, Community
from rest_framework.permissions import IsAuthenticated
from .serializers import InvitationSerializer
from django.urls import reverse


class InvitationViewSet(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')
        self.community = Community.objects.create(name='Test Community', owner=self.user1)
        self.invitation = Invitation.objects.create(
            inviter=self.user1, community=self.community, invitee=self.user2
        )
        self.community.members.add(self.user1)

    def test_send_existing_invite(self):
        self.client.force_authenticate(user=self.user1)
        
        response = self.client.post(
            reverse('invitation-send-invite'),
            {'community_id': self.community.id, 'invitee_username': self.user2.username}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Invitation.objects.count(), 1)

    def test_send_invite_invalid_community(self):
        self.client.force_authenticate(user=self.user1)
        valid_community = Community.objects.create(name='Valid Community', owner=self.user1)
        response = self.client.post(
            reverse('invitation-send-invite'),
            {'community_id': valid_community.id, 'invitee_username': self.user2.username}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_accept_invite(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(
            reverse('invitation-accept-invite', args=[self.invitation.id])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.community.members.filter(pk=self.user2.pk).exists())
        self.assertTrue(Invitation.objects.get(pk=self.invitation.id).accepted)

    def test_user_community_view(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(reverse('get_user_communities'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user_communities', response.data)
        self.assertEqual(len(response.data['user_communities']), 1)
        self.assertEqual(response.data['user_communities'][0], self.community.name)
