from django.db.models import Q
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Community
from .serializers import CommunitySerializer
from web_3_degenz.permissions import IsCommunityOwnerOrModerator

class CommunityListCreateView(generics.ListCreateAPIView):
    serializer_class = CommunitySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        queryset = Community.objects.filter(
            Q(privacy='public') |
            Q(privacy='private') |
            Q(members=user)
        ).order_by('-last_visited')
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CommunityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [IsCommunityOwnerOrModerator]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Store the previous members and moderator
        previous_members = list(instance.members.all())
        previous_moderator = instance.moderators.first()  # Get the previous moderator

        self.perform_update(serializer)

        # Get the new members and moderator
        new_members = list(instance.members.exclude(id__in=[user.id for user in previous_members]))
        new_moderator = instance.moderators.first()  # Get the new moderator

        response_data = serializer.data

        # Include the current members and moderator in the response
        current_members = [f'user:{member.username}' for member in instance.members.all()]
        current_moderator = f'user:{previous_moderator.username}' if previous_moderator else None

        # Modify the response to include the added member and moderator
        response_data['message'] = {
            'current_members': current_members,
            'current_moderator': current_moderator,
            'added_members': [f'user:{member.username}' for member in new_members],
            'added_moderator': f'user:{new_moderator.username}' if new_moderator else None,
            'removed_members': [],
            'removed_moderator': f'user:{previous_moderator.username}' if previous_moderator else None
        }

        return Response(response_data)

