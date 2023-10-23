from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

    
class Community(models.Model):

    PRIVACY_CHOICES = (
        ('public', 'Public'),
        ('private', 'Private'),
        ('hidden', 'Hidden'),
    )
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'owned_communities')
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User, related_name='communities_joined', blank=True)
    moderators = models.ManyToManyField(User, related_name='communities_moderated', blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', default='../default_post_qjpefy', blank=True)
    last_visited = models.DateTimeField(null=True, blank=True)
    privacy = models.CharField(max_length=20, choices=PRIVACY_CHOICES, default='public')

    def __str__(self):
        return self.name


