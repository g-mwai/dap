from django.db import models
from django.utils import timezone
from datetime import date
import math
from accounts.models import Profile
from posts.models import Industries

from django.conf import settings
User = settings.AUTH_USER_MODEL

class GigType(models.TextChoices):
    PART_TIME = 'part-time', 'Part-Time'
    FULL_TIME = 'full-time', 'Full-time'
    CONTRACT = 'contract', 'Contract'
    TEMPORARY = 'temporary', 'Temporary'
    INTERNSHIP = 'internship', 'Internship'

class Experience(models.TextChoices):
    ENTRY = 'entry level', 'Entry Level'
    MID = 'mid level', 'Mid Level'
    SENIOR = 'senior level', 'Senior Level'
    NO = 'no experience', 'No Experience'


class Gig(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=10000) 
    gig_type = models.CharField(
        max_length=50,
        choices=GigType.choices,
        default=GigType.CONTRACT
    )
    industry = models.CharField(
        max_length=50,
        choices=Industries.choices,
        default=Industries.UNCATEGORIZED
    )
    experience = models.CharField(
        max_length=50,
        choices=Experience.choices,
        default=Experience.ENTRY
    )
    apply_link = models.URLField(max_length=200, blank=True)
    flagged = models.BooleanField(default=False)
    report_count = models.IntegerField(default=0)

    max_apply = models.IntegerField(default=0)
    location = models.CharField(max_length=100)    
    timestamp = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(
        User, related_name="gig_posted_by", on_delete=models.CASCADE, null=True
    )

    def save(self, *args, **kwargs):
        author = self.posted_by
        author.wallet.balance -= 13
        author.wallet.total_spend += 13
        author.wallet.save()
        super().save(*args, **kwargs)
        
    def update_report_count(self):
        self.report_count = self.g_report.count()
        self.save(update_fields=['report_count'])
      
    def whenpublished(self):
        now = timezone.now()
        
        diff= now - self.timestamp

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds == 1:
                return str(seconds) +  "s"
            
            else:
                return str(seconds) + " s"

            

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + "m"
            
            else:
                return str(minutes) + "m"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + "h"

            else:
                return str(hours) + "h"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return str(days) + "d"

            else:
                return str(days) + "d"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            

            if months == 1:
                return str(months) + "mo"

            else:
                return str(months) + "mo"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + "yr"

            else:
                return str(years) + "yrs"

    # @property
    def poster_full(self):
        le_profile = Profile.objects.get(user=self.posted_by)
        name = le_profile.name
        return name
        
    def profile(self):
        profile = Profile.objects.get(user=self.posted_by)
        return profile

    @property
    def avatar(self):
        le_profile = Profile.objects.get(user=self.posted_by)
        avatar = le_profile.avatar
        return avatar
     

    def poster_bio(self):
        le_profile = Profile.objects.get(user=self.posted_by)
        bio = le_profile.bio
        return bio

    def is_verified(self):
        le_profile = Profile.objects.get(user=self.posted_by)
        is_verified = le_profile.is_verified
        return is_verified


    class Meta:
        ordering = ["-timestamp"]

class GigApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gig = models.ForeignKey(Gig, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'gig']
        
class Apply(models.Model):
    body = models.TextField(max_length=1000) 
    applicant = models.ForeignKey(
        User, related_name="apply_by", on_delete=models.CASCADE, null=True
    )
    gig = models.ForeignKey(
        Gig, related_name="related_gig", on_delete=models.CASCADE, null=True
    )
    
    def __str__(self):
        return self.applicant.username
