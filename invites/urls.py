from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserCommunityView, InvitationViewSet

router = DefaultRouter()
router.register(r'invitations', InvitationViewSet, basename='invitation')

urlpatterns = [
    path('get_user_communities/', UserCommunityView.as_view(), name='get_user_communities'),
    path('', include(router.urls)),
]
