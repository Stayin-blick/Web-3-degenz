from rest_framework import serializers
from .models import Invitation
from communities.models import Community
from django.contrib.auth.models import User

class InvitationSerializer(serializers.ModelSerializer):
    invitee_username = serializers.CharField(write_only=True)
    community = serializers.PrimaryKeyRelatedField(queryset=Community.objects.none())
    accepted = serializers.BooleanField(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['invitee_username'].choices = self.get_invitee_choices()
        self.fields['community'].queryset = Community.objects.filter(members=self.context['request'].user)

    def get_invitee_choices(self):
        inviter = self.context['request'].user
        followers = inviter.following.all()
        follower_usernames = [follower.followed.username for follower in followers]
        return [(username, username) for username in follower_usernames]

    def validate(self, data):
        inviter = self.context['request'].user
        invitee_username = data.get('invitee_username')
        community = data.get('community')

        if inviter.username == invitee_username:
            raise serializers.ValidationError("You cannot invite yourself.")

        if community.members.filter(username=invitee_username).exists():
            raise serializers.ValidationError("The user is already a member of the community.")

        if Invitation.objects.filter(inviter=inviter, community=community, invitee__username=invitee_username).exists():
            raise serializers.ValidationError("You have already invited this user to the community.")

        return data

    def save(self, **kwargs):
        inviter = self.context['request'].user
        community = self.validated_data['community']
        invitee_username = self.validated_data['invitee_username']

        # Check if the invitee is already a member of the community
        if community.members.filter(username=invitee_username).exists():
            raise serializers.ValidationError("The user is already a member of the community.")

        # Check if an invitation from the same inviter to the same community for the same invitee exists
        if Invitation.objects.filter(inviter=inviter, community=community, invitee__username=invitee_username).exists():
            raise serializers.ValidationError("You have already invited this user to the community.")

        # If everything is valid, create the invitation
        invitation = Invitation.objects.create(
            inviter=inviter,
            community=community,
            invitee=User.objects.get(username=invitee_username)
        )

        return invitation

    class Meta:
        model = Invitation
        fields = ['community', 'invitee_username', 'accepted']
