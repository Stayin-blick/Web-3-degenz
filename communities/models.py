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
    
    def update_moderators(self, moderators_to_add=None, moderators_to_remove=None):
        if moderators_to_add:
            self.moderators.add(*moderators_to_add)
        if moderators_to_remove:
            self.moderators.remove(*moderators_to_remove)
        self.save()

    def update_members(self, members_to_add=None, members_to_remove=None):
        if members_to_add:
            self.members.add(*members_to_add)
        if members_to_remove:
            self.members.remove(*members_to_remove)
        self.save()

    class Meta:
        ordering = ['-created_at']
