from rest_framework import serializers
from .models import Invitation
from communities.models import Community
from django.contrib.auth.models import User


class InvitationListSerializer(serializers.ModelSerializer):
    community_name = serializers.SerializerMethodField()

    class Meta:
        model = Invitation
        fields = ['id', 'inviter', 'community', 'invitee', 'created_at', 'accepted', 'community_name']

    def get_community_name(self, instance):
        """Get the community name."""
        return instance.community.name if instance.community else None


class InvitationSendSerializer(serializers.ModelSerializer):
    invitee_username = serializers.CharField(write_only=True)
    community = serializers.PrimaryKeyRelatedField(queryset=Community.objects.none())
    accepted = serializers.BooleanField(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['invitee_username'].choices = self.get_invitee_choices()
        self.fields['community'].queryset = Community.objects.filter(members=self.context['request'].user)

    def get_invitee_choices(self):
        inviter = self.context['request'].user
        follower_usernames = [follower.followed.username for follower in inviter.following.all()]
        return [(username, username) for username in follower_usernames]

    def validate(self, data):
        inviter = self.context['request'].user
        invitee_username = data.get('invitee_username')
        community = data.get('community')

        # Check if the inviter is a member of the community
        if not community.members.filter(username=inviter.username).exists():
            raise serializers.ValidationError("You are not a member of the community.")

        # Check if the invitee is not already a member of the community
        if community.members.filter(username=invitee_username).exists():
            raise serializers.ValidationError("The user is already a member of the community.")

        # Check if the invitee doesn't have a pending invite to the community
        if Invitation.objects.filter(community=community, invitee__username=invitee_username, accepted=None).exists():
            raise serializers.ValidationError("The user already has a pending invitation to the community.")

        # Check if the invitee has already been invited to the community
        if Invitation.objects.filter(community=community, invitee__username=invitee_username, accepted=False).exists():
            raise serializers.ValidationError("The user has already been invited to the community.")

        try:
            # Get the user object for the invitee
            invitee = User.objects.get(username=invitee_username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid username for invitee.")

        # Check if the inviter has not already sent an invite to the invitee
        if Invitation.objects.filter(inviter=inviter, community=community, invitee=invitee, accepted=None).exists():
            raise serializers.ValidationError("You have already sent an invitation to this user for the community.")

        return data

    def create(self, validated_data):
        inviter = self.context['request'].user
        community = validated_data['community']
        invitee_username = validated_data['invitee_username']

        try:
            # Get the user object for the invitee
            invitee = User.objects.get(username=invitee_username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid username for invitee.")

        # Create the invitation
        invitation = Invitation.objects.create(
            inviter=inviter,
            community=community,
            invitee=invitee,  # Set the invitee field
        )

        return invitation

    class Meta:
        model = Invitation
        fields = ['community', 'invitee_username', 'accepted']


class InvitationAcceptSerializer(serializers.ModelSerializer):
    accepted = serializers.BooleanField()

    def validate(self, data):
        # Ensure that the invitation being accepted belongs to the current user
        invitation = self.instance
        user = self.context['request'].user

        if invitation.invitee != user:
            raise serializers.ValidationError("You do not have permission to accept this invitation.")

        return data

    def update(self, instance, validated_data):
        accepted = validated_data['accepted']

        if accepted:
            # Accept the invitation and make the user a member of the community
            instance.accepted = True
            instance.save()
            instance.community.members.add(instance.invitee)
        else:
            # Decline the invitation and delete it
            instance.delete()

        return instance

    class Meta:
        model = Invitation
        fields = ['accepted']
