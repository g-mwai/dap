from django.db import models
from shops.models import Shop, Service
# Create your models here.
from django.conf import settings
User = settings.AUTH_USER_MODEL
import uuid

class Status(models.TextChoices):
    PENDING = 'pending', 'Pending'
    CONFIRMED = 'confirmed', 'Confirmed'
    CANCELED = 'canceled', 'Canceled'
    RESCHEDULE = 'reschedule', 'Reschedule'


class Booking(models.Model):
    identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='outgoing_bookings')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incoming_bookings')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True, blank=True, related_name='shop_booking')  # If the alert is related to a post
    is_read = models.BooleanField(default=False)
    status = models.CharField(
        max_length=50,
        choices=Status.choices,
        default=Status.PENDING
    ) 
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True, related_name='service_booking')  # If the alert is related to a post

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

    
        
    class Meta:
        ordering = ['-timestamp']