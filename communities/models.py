from django.db import models
from django.contrib.auth.models import User

    
class Community(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User)
    moderators = models.ManyToManyField(User, related_name = 'moderated_communities')
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', default='../default_post_qjpefy', blank=True)
