from django.db import models
from posts.models import Industries
from django_countries.fields import CountryField

from django.conf import settings
User = settings.AUTH_USER_MODEL
import uuid

class Service(models.Model):
    pass

class Product(models.Model):
    name = models.CharField(max_length=55)
    category = models.CharField(
        max_length=50,
        choices=Industries.choices,
        default=Industries.UNCATEGORIZED
    ) 
    about = models.TextField(max_length=10000) 
    dis_price = models.IntegerField(default=0)
    sale_price = models.IntegerField(default=0)
    image = models.ImageField(
         upload_to="product_img/", null=True, blank=True
    )
    def __str__(self):
        return self.name

class ProductImage(models.Model):
    image = models.ImageField(
         upload_to="product_img/", null=True, blank=True
    )
    product = models.ForeignKey(
        Product, related_name="product_img", on_delete=models.CASCADE
    )
    
class Location(models.Model):
    name = models.CharField(max_length=55)
    
    def __str__(self):
        return self.name

class Shop(models.Model): 
  
    owner = models.ForeignKey(
        User, related_name="shop_owner", on_delete=models.CASCADE, null=True
    )    
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)

    country = CountryField()
    services = models.ManyToManyField(Service, blank=True, related_name="shop_services")
    locations = models.ManyToManyField(Location, blank=True, related_name="shop_locations")
    bio = models.TextField(max_length=150)
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
    
    ext_link = models.URLField(max_length=200, blank=True)
 
class Review(models.Model):

    review_by = models.ForeignKey(
        User, related_name="review_by", on_delete=models.CASCADE, null=True
    )
    shop = models.ForeignKey(
        Shop, related_name="review_shop", on_delete=models.CASCADE
    )
    score = models.IntegerField(default=0)
    identifier = models.UUIDField(default=uuid.uuid4, editable=False)

    likes = models.ManyToManyField(User, blank=True, related_name="liked_reviews", symmetrical=False)
    dislikes = models.ManyToManyField(User, blank=True, related_name="disliked_reviews", symmetrical=False)
    body = models.TextField(max_length=500)
    reply_count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    flagged = models.BooleanField(default=False)
    report_count = models.IntegerField(default=0)

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

    def __int__(self):
        return self.id

class ReviewLike(models.Model):
    review = models.ForeignKey(
        Review, related_name="review_likes", on_delete=models.CASCADE
        )
    user = models.ForeignKey(
        User, related_name="user_likes_review", on_delete=models.CASCADE, null=True
    )
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

class ReviewReply(models.Model):

    reply_by = models.ForeignKey(
        User, related_name="review_reply_by", on_delete=models.CASCADE, null=True
    )
    review = models.ForeignKey(
        Review, related_name="shop_review_reply", on_delete=models.CASCADE
    )
    body = models.CharField(max_length=300)
    timestamp = models.DateTimeField(auto_now_add=True)
    flagged = models.BooleanField(default=False)

    

    
    @property
    def avatar(self):
        le_profile = Profile.objects.get(user=self.reply_by)
        avatar = le_profile.avatar
        return avatar  

    def is_verified(self):
        le_profile = Profile.objects.get(user=self.reply_by)
        is_verified = le_profile.is_verified
        return is_verified

    def le_profile(self):
        le_profile = Profile.objects.get(user=self.reply_by)
        return le_profile

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

    def __str__(self):
        return self.related_comment
