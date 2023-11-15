from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsCommunityOwnerOrModerator(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user in obj.moderators.all()


class IsCommunityMember(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return request.user in obj.community.members.all()


class IsPostOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user