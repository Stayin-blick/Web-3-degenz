from django.urls import path
from posts import views

urlpatterns = [
    path('posts/', views.PostList.as_view()),
    path('posts/<int:pk>/', views.PostDetail.as_view()),
    path('communities/<int:community_id>/posts/', views.CommunityPostList.as_view(), name='community-post-list'),
    path('communities/<int:community_id>/posts/<int:pk>/', views.CommunityPostDetail.as_view(), name='comunity-post-detail'),
]