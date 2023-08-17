from django.urls import path
from communities import views

urlpatterns = [
    path('communities/', views.CommunityList.as_view()),
    path('communities/<int:pk>/edit_community/', views.CommunityDetail.as_view(), name='edit_community'),
]
