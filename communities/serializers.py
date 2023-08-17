from rest_framework import serializers
from .models import Community

class CommunitySerializer(serializers.ModelSerializer):

    active_moderators = serializers.SerializerMethodField()

    def get_active_moderators(self, obj):
        moderators = obj.moderators.all()
        return [{'username': moderator.username} for moderator in moderators]

    class Meta:
        model = Community
        fields = [
            'id', 'name', 'owner', 'moderators',
            'created_at', 'privacy', 'active_moderators'
        ]
