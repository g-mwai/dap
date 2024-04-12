from django.db import models
from posts.models import Post, Comment
from django.conf import settings
User = settings.AUTH_USER_MODEL
from gigs.models import Gig
# Create your models here.
from accounts.models import Profile
from django.utils import timezone
import math
from ckeditor.fields import RichTextField


class Content(models.TextChoices):
    NSFW = 'nsfw', 'Nsfw'
    SPAM = 'spam', 'Spam'
    MISINFO = 'misinformation', 'Misinformation'
    OFFENSIVE = 'offensive', 'Offensive'
    HATE = 'hate', 'Hate'

class Priority(models.TextChoices):
    LOW = 'low', 'Low'
    MOD = 'moderate', 'Moderate'
    HIGH = 'high', 'High'

class Policies(models.TextChoices):
    PRIVACY = 'privacy', 'Privacy'
    GUIDE = 'guidelines', 'Guidelines'
    TERMS = 'terms', 'Terms'
    LICENSE = 'license', 'License'
    MANIFESTO = 'manifesto', 'Manifesto'

class Report(models.Model):
    post = models.ForeignKey(
        Post, related_name="report", on_delete=models.CASCADE
        )
    content = models.CharField(
        max_length=50,
        choices=Content.choices,
        default=Content.SPAM
    ) 
    user = models.ForeignKey(
        User, related_name="report_by", on_delete=models.CASCADE, null=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)


    def is_verified(self):
        le_profile = Profile.objects.get(user=self.user)
        is_verified = le_profile.is_verified
        return is_verified
    

    def save(self, *args, **kwargs):
        is_new = not self.pk
        super(Report, self).save(*args, **kwargs)
        
        # Update the report_count field in the related Post model
        if is_new:
            self.post.update_report_count()

    def delete(self, *args, **kwargs):
        super(Report, self).delete(*args, **kwargs)
        
        # Update the report_count field in the related Post model
        self.post.update_report_count()

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

 
    class Meta:
        ordering = ["-timestamp"]

class ReportGig(models.Model):
    gig = models.ForeignKey(
        Gig, related_name="g_report", on_delete=models.CASCADE
        )
    content = models.CharField(
        max_length=50,
        choices=Content.choices,
        default=Content.SPAM
    ) 
    user = models.ForeignKey(
        User, related_name="gig_report_by", on_delete=models.CASCADE, null=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

class ReportComment(models.Model):
    comment = models.ForeignKey(
        Comment, related_name="c_report", on_delete=models.CASCADE
        )
    content = models.CharField(
        max_length=50,
        choices=Content.choices,
        default=Content.SPAM
    ) 
    user = models.ForeignKey(
        User, related_name="comment_report_by", on_delete=models.CASCADE, null=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

class ReportBug(models.Model):
    body = models.TextField(max_length=10000) 
    priority = models.CharField(
        max_length=50,
        choices=Priority.choices,
        default=Priority.LOW
    ) 
    user = models.ForeignKey(
        User, related_name="bug_report_by", on_delete=models.CASCADE, null=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-timestamp"]

class Policy(models.Model):
    title = models.CharField(max_length=100)    
    body = RichTextField(null=True, blank=True, 
    config_name="special")
    author = models.ForeignKey(
        User, related_name="policy_author", on_delete=models.CASCADE, null=True
    )
    pol = models.CharField(
        max_length=50,
        choices=Policies.choices,
        default=Policies.PRIVACY
    ) 
    timestamp = models.DateTimeField(auto_now_add=True)


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

    class Meta:
        ordering = ["-timestamp"]   