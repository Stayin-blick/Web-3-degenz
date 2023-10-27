from django.urls import path
from followers import views

urlpatterns = [
    path('followers/', views.FollowerList.as_view()),
    path('followers/<int:pk>/', views.FollowerDetail.as_view()),
    path('followed-accounts/', views.FollowedAccountsList.as_view(), name='followed-accounts-list'),
]
