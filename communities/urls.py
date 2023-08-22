from django.urls import path
from communities import views

urlpatterns = [
    path('communities/', views.CommunityList.as_view(), name='community_list'),
    path('communities/<int:pk>/posts/', views.CommunityPostList.as_view(), name='community_post_list'),
    path('communities/<int:pk>/edit_community/', views.CommunityDetail.as_view(), name='edit_community'),
]
