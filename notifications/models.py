from django.db import models
from django.utils import timezone
from accounts.models import Profile
from posts.models import Post
from django.conf import settings
User = settings.AUTH_USER_MODEL
from posts.models import Post

class Alert(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_alerts')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_alerts')
    ALERT_TYPES = (
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('reply', 'Reply'),
        ('delete', 'Delete'),
        ('fine', 'Fine'),
        ('keep', 'Keep'),
        ('bug', 'Bug'),
        ('follow', 'Follow'),
    )
    alert_type = models.CharField(max_length=10, choices=ALERT_TYPES)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)  # If the alert is related to a post
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username} {self.alert_type}d your post'

    # @property
    def poster_full(self):
        le_profile = Profile.objects.get(user=self.sender)
        name = le_profile.name
        return name
        
    def profile(self):
        profile = Profile.objects.get(user=self.sender)
        return profile

    @property
    def avatar(self):
        le_profile = Profile.objects.get(user=self.sender)
        avatar = le_profile.avatar
        return avatar
     

    def poster_bio(self):
        le_profile = Profile.objects.get(user=self.sender)
        bio = le_profile.bio
        return bio

    def is_verified(self):
        le_profile = Profile.objects.get(user=self.sender)
        is_verified = le_profile.is_verified
        return is_verified

    def post_id(self):
        le_id = Post.objects.filter(id)
        return le_id
        
    class Meta:
        ordering = ['-timestamp']