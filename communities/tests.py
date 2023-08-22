from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Community

class CommunityAPITestCase(APITestCase):
    def setUp(self):
        self.user_owner = User.objects.create_user(username='owner', password='password123')
        self.user_moderator = User.objects.create_user(username='moderator', password='password123')
        self.user_member = User.objects.create_user(username='member', password='password123')

        self.community_data = {
            'name': 'Test Community',
            'owner': self.user_owner.id,
            'privacy': 'public'
        }

        self.client.force_authenticate(user=self.user_owner)

    def test_community_creation(self):
        self.client.force_authenticate(user=self.user_owner)
        response = self.client.post(reverse('community-list'), data=self.community_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Community.objects.count(), 1)

    def test_moderator_management(self):
        community = Community.objects.create(name='Test Community', owner=self.user_owner)

        self.client.force_authenticate(user=self.user_owner)

        # Add moderator
        data = {'moderators_to_add': [self.user_moderator.id]}
        response = self.client.put(reverse('edit_community', kwargs={'pk': community.id}), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user_moderator in community.moderators.all())

        # Remove moderator
        data = {'moderators_to_remove': [self.user_moderator.id]}
        response = self.client.put(reverse('edit_community', kwargs={'pk': community.id}), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.user_moderator in community.moderators.all())

    def test_member_management(self):
        community = Community.objects.create(name='Test Community', owner=self.user_owner)

        self.client.force_authenticate(user=self.user_owner)

        # Add member
        data = {'members_to_add': [self.user_member.id]}
        response = self.client.put(reverse('edit_community', kwargs={'pk': community.id}), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user_member in community.members.all())

        # Remove member
        data = {'members_to_remove': [self.user_member.id]}
        response = self.client.put(reverse('edit_community', kwargs={'pk': community.id}), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.user_member in community.members.all())

    def test_invite_and_join_community(self):
        # Create a community and an invited user
        community = Community.objects.create(name='Test Community', owner=self.user_owner)
        invited_user = User.objects.create_user(username='invited', password='password123')

        # Authenticate the owner and send an invitation to the invited user
        self.client.force_authenticate(user=self.user_owner)
        response = self.client.post(reverse('community-invite', kwargs={'pk': community.id}), data={'username': invited_user.username})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Authenticate the invited user and accept the invitation
        self.client.force_authenticate(user=invited_user)
        response = self.client.post(reverse('community-accept-invite', kwargs={'pk': community.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the invited user is now a member of the community
        self.assertTrue(invited_user in community.members.all())
