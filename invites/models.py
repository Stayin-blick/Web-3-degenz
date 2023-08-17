from django.db import models
from django.contrib.auth.models import User
from communities.models import Community

class Invitation(models.Model):
    inviter = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    invitee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitations_received')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['inviter', 'community', 'invitee']
        ordering = ['-created_at']
