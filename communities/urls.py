from django.urls import path
from communities import Community

urlpatterns = [
    path('communities/', views.CommunitiesList.as_view()),
]
