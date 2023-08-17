from django.urls import path
from communities import views

urlpatterns = [
    path('communities/', views.CommunityList.as_view()),
]
