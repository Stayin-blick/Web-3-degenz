from django.urls import path
from communities import views

urlpatterns = [
    path('communities/', views.CommunityList.as_view(), name='community-list'),
    path('communities/<int:pk>/list_posts/', views.CommunityDetail.as_view(), name='community-list-posts'),
    path('communities/<int:pk>/edit_community/', views.CommunityDetail.as_view(), name='edit_community'),
    path('communities/<int:pk>/update_moderators/', views.CommunityDetail.as_view(), name='community-update-moderators'),
    path('communities/<int:pk>/update_members/', views.CommunityDetail.as_view(), name='community-update-members'),
    path('communities/<int:pk>/add_moderators/', views.CommunityDetail.as_view(), name='community-add-moderators'),
    path('communities/<int:pk>/remove_moderators/', views.CommunityDetail.as_view(), name='community-remove-moderators'),
    path('communities/<int:pk>/remove_member/', views.CommunityDetail.as_view(), name='community-remove-member'),
    path('communities/<int:pk>/remove_post/', views.CommunityDetail.as_view(), name='community-remove-post'),
]
