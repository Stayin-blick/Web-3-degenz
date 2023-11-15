from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

    
class Community(models.Model):
    PRIVACY_CHOICES = (
        ('public', 'Public'),
        ('private', 'Private'),
        ('hidden', 'Hidden'),
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_communities')
    owner_username = models.CharField(max_length=255, blank=True)  
    moderators = models.ManyToManyField(User, related_name='communities_moderated', blank=True)
    moderators_usernames = models.TextField(blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User, related_name='communities_joined', blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', default='../default_post_qjpefy', blank=True)
    last_visited = models.DateTimeField(null=True, blank=True)
    privacy = models.CharField(max_length=20, choices=PRIVACY_CHOICES, default='public')

    def save(self, *args, **kwargs):
        # Update owner's username
        if self.owner:
            self.owner_username = self.owner.username

        # Update moderators' usernames
        if self.moderators.exists():
            self.moderators_usernames = ','.join([moderator.username for moderator in self.moderators.all()])
        else:
            self.moderators_usernames = ''

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class CommunityPost(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='community_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    content = models.TextField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

