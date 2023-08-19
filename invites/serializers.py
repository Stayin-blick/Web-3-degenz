from rest_framework import serializers
from .models import Invitation

class InvitationSerializer(serializers.ModelSerializer):
    invitee_username = serializers.CharField()
    community_name = serializers.SerializerMethodField()
    accepted = serializers.BooleanField(read_only=True)

    class Meta:
        model = Invitation
        fields = ['community_name', 'invitee_username', 'accepted']

    def get_community_name(self, obj):
        return obj.community.name