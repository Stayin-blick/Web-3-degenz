from django.urls import path
from . import views

urlpatterns = [
    path('send_invite/', views.send_invite, name='send_invite'),
    path('accept_invite/<int:invitation_id>/', views.accept_invite, name='accept_invite'),
]
