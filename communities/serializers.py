from rest_framework import serializers
from .models import Community

class CommunitySerializer(serializers.ModelSerializer):

    active_moderators = serializers.StringRelatedField(many=True, source='moderators')

    class Meta:
        model = Community
        fields = [
            'id', 'name', 'owner', 'moderators',
            'created_at', 'privacy', 'active_moderators'
        ]
