import imp 
from pyexpat import model
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from datetime import date
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# from common.templatetags.common_tags import is_document_file_image
from django_countries.fields import CountryField

class Gender(models.TextChoices):
    MALE = 'male', 'Male'
    FEMALE = 'female', 'Female'
    UNSPECIFIED = 'unspecified', 'Unspecified'

class ProfileType(models.TextChoices):
    PERSONAL = 'personal', 'Personal'
    BUSINESS = 'business', 'Business'
    NON_PROFIT = 'non profit', 'Non Profit'
    GOV = 'government', 'Government'


class Industries(models.TextChoices):    
    TECHNOLOGY = 'technology', 'Technology'
    FINANCE = 'finance', 'Finance'
    HEALTHCARE = 'healthcare', 'Healthcare'
    EDUCATION = 'education', 'Education'
    RETAIL = 'retail', 'Retail'
    BEAUTY = 'beauty & wellness', 'Beauty & Wellness'
    HOSPITALITY = 'hospitality', 'Hospitality'
    PROFESSIONAL_SERVICES = 'professional services', 'Professional Services'
    FOOD = 'Food', 'Food'
    REAL_ESTATE = 'real estate', 'Real Estate'
    ART = 'art & culture', 'Art & Culture'
    SPORTS = 'sports & fitness', 'Sports & Fitness'
    EVENTS = 'events & entertainment', 'Events & Entertainment'
    PUBLIC_SERVICE = 'public service', 'Public Service'
    BLUE_COLLAR = 'blue collar', 'Blue Collar'
    NON_PROFIT = 'non profit', 'Non Profit'
    MANUFACTURING = 'manufacturing', 'Manufacturing'
    TELECOMMUNICATIONS = 'telecommunications', 'Telecommunications'
    ENGINEERING = 'engineering', 'Engineering'
    UNCATEGORIZED = 'uncategorized', 'Uncategorized'

class User(AbstractUser):
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    email = models.EmailField(max_length=254, null=True)

    # def __str__(self):
    #     return self.username

class UserCount(models.Model):
    date = models.DateField()
    count = models.IntegerField(default=0)

    class Meta:
        ordering = ["date"]
    
class Profile(models.Model): 
  
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile" )
    name = models.CharField(max_length=50)
    country = CountryField()
    job_title = models.CharField(max_length=50)

    location = models.CharField(max_length=50)
    birthday = models.DateField(default=date.today)
    bio = models.TextField(max_length=150)
    user_tokens = models.IntegerField(default=50)
    is_verified = models.BooleanField(default=False)
    following = models.ManyToManyField(
        "self", blank=True, related_name="followers", symmetrical=False
    )
    industry = models.CharField(
        max_length=50,
        choices=Industries.choices,
        default=Industries.UNCATEGORIZED
    ) 
    avatar = models.ImageField(
         upload_to="profile_pics/", 
        #  default='profile_pics/default_avatar.jpg',
         null=True, 
         blank=True
    )   
    cover_image = models.ImageField(
         upload_to="cover_image/", null=True, blank=True
    )
    gender = models.CharField(
        max_length=50,
        choices=Gender.choices,
        default=Gender.UNSPECIFIED
    )
    profile_type = models.CharField(
        max_length=50,
        choices=ProfileType.choices,
        default=ProfileType.PERSONAL
    )
    ext_link = models.URLField(max_length=200, blank=True)
 
    
 
    def __str__(self):
        return self.user.username
   
    @property
    def username(self):
        user = self.user.username
        return user


    @receiver(post_save, sender=User) 
    def create_profile(sender, instance, created, **kwargs):
        if created and not hasattr(instance, 'profile'):
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_profile(sender, instance, **kwargs):
        instance.profile.save()

    

class Portfolio(models.Model):
    profile = models.ForeignKey(
        Profile, related_name="profile_portfolio", on_delete=models.CASCADE, null=True
    )

class PasswordChangeRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=5, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        # Check if the link is expired (valid for 5 minutes)
        return timezone.now() > self.created_at + timezone.timedelta(minutes=5)