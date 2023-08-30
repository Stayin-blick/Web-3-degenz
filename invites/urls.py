from django.urls import path
from invites import views

urlpatterns = [
    path('invitations/', views.InvitationListView.as_view(), name='invitation-received-list'),
    path('invitations/create/', views.InvitationCreateView.as_view(), name='invitation-create'),
    path('invitations/<int:pk>/accept/', views.InvitationAcceptView.as_view(), name='invitation-accept'),
]
