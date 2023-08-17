from django.urls import path
from communities import views

urlpatterns = [
    path('communities/', views.CommunitiesList.as_view()),
]
