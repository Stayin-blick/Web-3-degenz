from django.db import models
from django.contrib.auth.models import User

    
class Community(models.Model):
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'owned_communities')
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User, related_name='joined_communities')
    moderators = models.ManyToManyField(User, related_name='moderated_communities', blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', default='../default_post_qjpefy', blank=True)

    PRIVACY_CHOICES = (
        ('public', 'Public'),
        ('private', 'Private'),
        ('hidden', 'Hidden'),
    )
    
    privacy = models.CharField(
        max_length=10, choices=PRIVACY_CHOICES, default='public'
    )

    class Meta:
        ordering = ['-created_at']
