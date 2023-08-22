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
        self.user_non_member = User.objects.create_user(username='nonmember', password='password123')

        self.community_data = {
            'name': 'Test Community',
            'owner': self.user_owner.id,
            'privacy': 'public'
        }

        self.client.force_authenticate(user=self.user_owner)

    def test_community_creation(self):
        response = self.client.post(reverse('community-list'), data=self.community_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Community.objects.count(), 1)

    def test_moderator_management(self):
        community = Community.objects.create(name='Test Community', owner=self.user_owner)

        # Add moderator
        data = {'moderators_to_add': [self.user_moderator.id]}
        response = self.client.put(reverse('community-update-moderators', kwargs={'pk': community.id}), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user_moderator in community.moderators.all())

        # Remove moderator
        data = {'moderators_to_remove': [self.user_moderator.id]}
        response = self.client.put(reverse('community-update-moderators', kwargs={'pk': community.id}), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.user_moderator in community.moderators.all())

    def test_member_management(self):
        community = Community.objects.create(name='Test Community', owner=self.user_owner)

        # Add member
        data = {'members_to_add': [self.user_member.id]}
        response = self.client.put(reverse('community-update-members', kwargs={'pk': community.id}), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user_member in community.members.all())

        # Remove member
        data = {'members_to_remove': [self.user_member.id]}
        response = self.client.put(reverse('community-update-members', kwargs={'pk': community.id}), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.user_member in community.members.all())

    def test_invite_non_member(self):
        community = Community.objects.create(name='Test Community', owner=self.user_owner)

        # Non-member attempting to invite another user
        self.client.force_authenticate(user=self.user_non_member)
        response = self.client.post(reverse('community-invite', kwargs={'pk': community.id}), data={'username': self.user_member.username})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

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

    def test_member_post_creation(self):
        community = Community.objects.create(name='Test Community', owner=self.user_owner)
        self.client.force_authenticate(user=self.user_member)

        post_data = {'content': 'This is a test post.'}
        response = self.client.post(reverse('community-post-list', kwargs={'pk': community.id}), data=post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(community.posts.count(), 1)

    def test_non_member_post_creation(self):
        community = Community.objects.create(name='Test Community', owner=self.user_owner)
        self.client.force_authenticate(user=self.user_non_member)

        post_data = {'content': 'This is a test post.'}
        response = self.client.post(reverse('community-post-list', kwargs={'pk': community.id}), data=post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(community.posts.count(), 0)

    def test_invalid_moderator_addition(self):
        community = Community.objects.create(name='Test Community', owner=self.user_owner)
        community.moderators.add(self.user_moderator)  # Adding moderator
        
        self.client.force_authenticate(user=self.user_owner)
        data = {'moderators_to_add': [self.user_moderator.id]}  # Trying to add the same moderator
        response = self.client.put(reverse('edit_community', kwargs={'pk': community.id}), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Invalid moderator IDs.')

    def test_unauthenticated_community_creation(self):
        response = self.client.post(reverse('community-list'), data=self.community_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_non_owner_moderator_management(self):
        # Attempting to add a moderator as a non-owner
        community = Community.objects.create(name='Test Community', owner=self.user_owner)
        self.client.force_authenticate(user=self.user_member)
        data = {'moderators_to_add': [self.user_moderator.id]}
        response = self.client.put(reverse('edit_community', kwargs={'pk': community.id}), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'You are not the owner of this community.')

    def test_private_community_access(self):
        community = Community.objects.create(name='Private Community', owner=self.user_owner, privacy='private')
        self.client.force_authenticate(user=self.user_member)
        response = self.client.get(reverse('community-detail', kwargs={'pk': community.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_private_community_access_non_member(self):
        community = Community.objects.create(name='Private Community', owner=self.user_owner, privacy='private')
        response = self.client.get(reverse('community-detail', kwargs={'pk': community.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_creation(self):
        community = Community.objects.create(name='Test Community', owner=self.user_owner)
        self.client.force_authenticate(user=self.user_member)
        post_data = {'content': 'This is a test post'}
        response = self.client.post(reverse('community-post-list', kwargs={'pk': community.id}), data=post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)

    def test_post_edit(self):
        community = Community.objects.create(name='Test Community', owner=self.user_owner)
        post = Post.objects.create(content='Initial content', owner=self.user_member, community=community)
        self.client.force_authenticate(user=self.user_member)
        updated_content = 'Updated content'
        response = self.client.put(reverse('post-detail', kwargs={'pk': post.id}), data={'content': updated_content}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertEqual(post.content, updated_content)

