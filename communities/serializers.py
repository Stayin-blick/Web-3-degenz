from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Community
from posts.serializers import PostSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class CommunitySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    members_count = serializers.SerializerMethodField()
    active_moderators = UserSerializer(many=True, read_only=True, source='moderators')
    posts = PostSerializer(many=True, read_only=True)

    def get_members_count(self, obj):
        return obj.members.count()

    class Meta:
        model = Community
        fields = [
            'id', 'name', 'owner', 'members_count',
            'created_at', 'privacy', 'active_moderators',
            'posts'
        ]
