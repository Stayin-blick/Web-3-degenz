from django.urls import path
from communities import views

urlpatterns = [
    path('communities/', views.CommunityListCreateView.as_view(), name='community_list'),
    path('communities/<int:pk>/edit_community/', views.CommunityDetailView.as_view(), name='edit_community'),
]
