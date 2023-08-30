from django.db import models
from django.contrib.auth.models import User
from communities.models import Community

class Invitation(models.Model):
    id = models.AutoField(primary_key=True)
    inviter = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    invitee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitations_received')
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False) 

    class Meta:
        unique_together = ['inviter', 'community', 'invitee']
        ordering = ['-created_at']
