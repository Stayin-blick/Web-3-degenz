from rest_framework import serializers
from .models import Invitation

class InvitationSerializer(serializers.ModelSerializer):
    invitee_username = serializers.CharField()

    class Meta:
        model = Invitation
        fields = ['invitee_username']
