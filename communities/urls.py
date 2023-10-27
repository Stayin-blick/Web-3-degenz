from django.urls import path
from communities import views

urlpatterns = [
    path('communities/', views.CommunityListCreateView.as_view(), name='community-list'),
    path('communities/<int:pk>/edit_community/', views.CommunityDetailView.as_view(), name='edit_community'),
    path('communities/<int:pk>/homepage/', views.CommunityPostListCreateView.as_view(), name='community-homepage'),
    path('communities/<int:pk>/posts/', views.CommunityPostListCreateView.as_view(), name='community-post-list'),
    path('communities/posts/<int:pk>/', views.CommunityPostDetailView.as_view(), name='community-post-detail'),
]
