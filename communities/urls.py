from django.urls import path
from communities import views

urlpatterns = [
    path('communities/', views.CommunityListCreateView.as_view(), name='community-list'),
    path('communities/<int:pk>/edit/', views.CommunityEditView.as_view(), name='edit_community'),
    path('communities/<int:pk>/edit_community/', views.CommunityDetailView.as_view(), name='edit_community'),
    path('communities/<int:pk>/info/', views.CommunityInfoView.as_view(), name='community-info'),
    path('communities/<int:pk>/homepage/', views.CommunityPostListCreateView.as_view(), name='community-homepage'),
    path('communities/<int:pk>/posts/', views.CommunityPostListCreateView.as_view(), name='community-post-list'),
    path('communities/posts/<int:pk>/', views.CommunityPostDetailView.as_view(), name='community-post-detail'),
    path('communities/posts/<int:pk>/delete/', views.UserPostDeleteView.as_view(), name='delete_user_post'),
    path('communities/<int:pk>/delete_post/<int:post_id>/', views.CommunityDetailView.as_view(), name='delete_post'),
    path('communities/<int:pk>/remove_member/', views.CommunityDetailView.as_view(), name='remove_member'),
]