from django.urls import path
from communities import views

urlpatterns = [
    path('communities/', views.CommunityListCreateView.as_view(), name='community-list'),
    path('communities/<int:pk>/edit_community/', views.CommunityDetailView.as_view(), name='edit_community'),
    # path('communities/<int:pk>/home_page/', views.CommunityDetailView.as_view(), name='<int:pk>'s_hompage'),
]
