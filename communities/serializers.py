from rest_framework import serializers
from .models import Community, CommunityPost

class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = '__all__'


class CommunityPostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    community_id = serializers.PrimaryKeyRelatedField(queryset=Community.objects.all())
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = CommunityPost
        fields = [
            'id', 'owner', 'is_owner', 'created_at', 'updated_at',
            'title', 'content', 'image', 'community_id',
            'likes_count', 'comments_count'
        ]


class CommunityEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ['owner', 'moderators', 'name', 'image', 'members', 'content', 'privacy']