from django.db import models
from accounts.models import Profile
from django.utils import timezone
import math
from datetime import date
# from wallet.models import Wallet
# from forums.models import Forum
from django.conf import settings
User = settings.AUTH_USER_MODEL
import uuid


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


class PostType(models.TextChoices):
    THREAD = 'thread', 'Thread'
    PRODUCT = 'product', 'Product'
    BLOG = 'blog', 'Blog'
    SELL = 'sell', 'Sell'
    PROJECT = 'project', 'Project'

class SellType(models.TextChoices):
    PRODUCT = 'product', 'Product'
    SERVICE = 'service', 'Service'
    DIGITAL = 'digital', 'Digital'
    EVENT = 'event', 'Event'
    FUNDRAISER = 'fundraiser', 'Fundraiser'
    UNCATEGORIZED = 'uncategorized', 'Uncategorized'

class CTA(models.TextChoices):
    BUY  = 'buy now', 'Buy Now'
    CONTACT = 'contact', 'Contact'
    SHOP= 'shop now', 'Shop Now'
    REGISTER= 'Register', 'Register'
    SUBSCRIBE= 'subscribe', 'Subscribe'
    DONATE= 'donate', 'Donate'
    GET_STARTED= 'get started', 'Get Started'

class ProjectCTA(models.TextChoices):
    WEBSITE = 'visit website', 'Visit Website'
    CONTACT = 'contact ', 'Contact'
    LEARN= 'learn more', 'Learn More'
    JOIN= 'join us', 'Join Us'
    DONATE= 'donate', 'Donate'

class Progress(models.TextChoices):
    IN_PROGRESS = 'in progress ', 'In Progress'
    COMPLETED= 'completed', 'Completed'
    STARTING_SOON= 'starting soon', 'Starting Soon'

class Categories(models.TextChoices):
    CLOTHING = 'clothing', 'Clothing'
    GITFS = 'gifts', 'Gifts'
    ACCESORIES = 'accessories', 'Accessories'
    ELECTRONICS = 'electronics', 'Electronics'
    MOMBABY = 'Mom & Baby', 'Mom & baby'
    UNCATEGORIZED = 'uncategorized', 'Uncategorized'


class View(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='views')
    viewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_viewer")
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def view_count(self):
        return self.views.count()

class Tag(models.Model):
    name = models.CharField(max_length=55)
    category = models.CharField(
        max_length=50,
        choices=Categories.choices,
        default=Categories.UNCATEGORIZED
    )

    def __str__(self):
        return self.name

class Post(models.Model):
    post_image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="post_tags", symmetrical=False)
    identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    progress = models.CharField(
        max_length=50,
        choices=Progress.choices,
        default=Progress.COMPLETED
    ) 
    posted_by = models.ForeignKey(
        User, related_name="posted_by", on_delete=models.CASCADE, null=True
    )     
    industry = models.CharField(
        max_length=50,
        choices=Industries.choices,
        default=Industries.UNCATEGORIZED
    ) 
    sell_type = models.CharField(
        max_length=50,
        choices=SellType.choices,
        default=SellType.UNCATEGORIZED
    ) 
    post_type = models.CharField(
        max_length=50,
        choices=PostType.choices,
        default=PostType.THREAD
    )  
    category = models.CharField(
        max_length=50,
        choices=Categories.choices,
        default=Categories.UNCATEGORIZED
    )
    is_pinned = models.BooleanField(default=False)
    closing_date = models.DateField(default=date.today)
    size = models.CharField(max_length=55)

    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name="liked_posts", symmetrical=False)
    dislikes = models.ManyToManyField(User, blank=True, related_name="disliked_posts", symmetrical=False)
    comment_count = models.IntegerField(default=0)
    bookmarked_users = models.ManyToManyField(User, blank=True, related_name="bookmarked_posts")
    flagged = models.BooleanField(default=False)
    headline = models.CharField(max_length=100, blank=True)
    report_count = models.IntegerField(default=0)
    body = models.TextField(max_length=10000) 
    donations = models.IntegerField(default=0)
    trade_vol = models.IntegerField(default=0)
    min_price = models.IntegerField(default=0)
    max_price = models.IntegerField(default=0)

    cta = models.CharField(
        max_length=50,
        choices=CTA.choices,
        default=CTA.SHOP
    )
    project_cta = models.CharField(
        max_length=50,
        choices=ProjectCTA.choices,
        default=ProjectCTA.WEBSITE
    )
    cta_link = models.URLField(max_length=200, blank=True)
    flagged = models.BooleanField(default=False)



    def save(self, *args, **kwargs):
        if self.post_type == 'thread':
            # Get the author of the post
            author = self.posted_by
            # Deduct 8 coins from the wallet balance
            author.wallet.balance -= 8
            # Add 8 coins to the total spend
            author.wallet.total_spend += 8
            # Save the wallet
            author.wallet.save()
        elif self.post_type == 'sell':
            # Get the author of the post
            author = self.posted_by
            # Deduct 8 coins from the wallet balance
            author.wallet.balance -= 13
            # Add 8 coins to the total spend
            author.wallet.total_spend += 13
            # Save the wallet
            author.wallet.save()
        
        elif self.post_type == 'project':
            # Get the author of the post
            author = self.posted_by
            # Deduct 8 coins from the wallet balance
            author.wallet.balance -= 5
            # Add 8 coins to the total spend
            author.wallet.total_spend += 5
            # Save the wallet
            author.wallet.save()
        super().save(*args, **kwargs)

    def update_report_count(self):
        self.report_count = self.report.count()
        self.save(update_fields=['report_count'])
        
    @property
    def view_count(self):
        return self.views.count()
    
    
    def earn_coins_for_views(self):
        # Get the author of the post
        author = self.posted_by

        # Calculate the number of views
        views = self.views.count()

        # Credit the author's wallet
        author.wallet.balance += views
        author.wallet.total_earn += views
        author.wallet.save()
    
    
    def upvote(self, user):
        self.likes.add(user)
        self.dislikes.remove(user)
        self.save()

    def downvote(self, user):
        self.likes.remove(user)
        self.dislikes.add(user)
        self.save()

    @property
    def vote_count(self):
        likes = self.likes.count()
        dislikes = self.dislikes.count()
        votes = likes - dislikes
        return votes
    

    @property
    def total_votes(self):
        total = self.likes.count() + self.dislikes.count()
        return total
    
   
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



class ProductImage(models.Model):
    image = models.ImageField(
         upload_to="post_img/", null=True, blank=True
    )
    post = models.ForeignKey(
        Post, related_name="prod_img", on_delete=models.CASCADE
    )
   

class Option(models.Model):
    option_image = models.ImageField(upload_to='post_images/', null=True, blank=True)
  
    post = models.ForeignKey(
        Post, related_name="post_option", on_delete=models.CASCADE
        )
    title = models.CharField(max_length=100)
    # votes = models.ManyToManyField(User, blank=True, related_name="votes")


class Like(models.Model):
    post = models.ForeignKey(
        Post, related_name="post_likes", on_delete=models.CASCADE
        )
    user = models.ForeignKey(
        User, related_name="profile_likes", on_delete=models.CASCADE, null=True
    )
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post
    
class Comment(models.Model):
    comment_image = models.ImageField(upload_to='post_images/', null=True, blank=True)

    comment_by = models.ForeignKey(
        User, related_name="comment_by", on_delete=models.CASCADE, null=True
    )
    parent_post = models.ForeignKey(
        Post, related_name="parent_post", on_delete=models.CASCADE
    )
    likes = models.ManyToManyField(User, blank=True, related_name="liked_comments", symmetrical=False)
    dislikes = models.ManyToManyField(User, blank=True, related_name="disliked_comments", symmetrical=False)
    body = models.TextField(max_length=500)
    reply_count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    flagged = models.BooleanField(default=False)
    report_count = models.IntegerField(default=0)
    bookmarked_users = models.ManyToManyField(User, blank=True, related_name="bookmarked_comments")

    def name(self):
        le_profile = Profile.objects.get(user=self.comment_by)
        name = le_profile.name
        return name
     
    def update_report_count(self):
        self.report_count = self.c_report.count()
        self.save(update_fields=['report_count'])
      
    def poster_bio(self):
        le_profile = Profile.objects.get(user=self.posted_by)
        bio = le_profile.bio
        return bio

    def upvote(self, user):
        self.likes.add(user)
        self.dislikes.remove(user)
        self.save()

    def downvote(self, user):
        self.likes.remove(user)
        self.dislikes.add(user)
        self.save()

    def is_verified(self):
        le_profile = Profile.objects.get(user=self.comment_by)
        is_verified = le_profile.is_verified
        return is_verified
    
    @property
    def like_count(self):
        return self.likes.count()

    @property
    def vote_count(self):
        likes = self.likes.count()
        dislikes = self.dislikes.count()
        votes = likes - dislikes
        return votes
    
  
    def related_poster(self):
        related = self.parent_post.posted_by
        le_profile = Profile.objects.get(user=related)
        return le_profile
       
    @property
    def avatar(self):
        le_profile = Profile.objects.get(user=self.comment_by)
        avatar = le_profile.avatar
        return avatar
    
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
        ordering = ["timestamp"]

    def __str__(self):
        return self.body

class CommentLike(models.Model):
    comment = models.ForeignKey(
        Comment, related_name="comment_likes", on_delete=models.CASCADE
        )
    user = models.ForeignKey(
        User, related_name="user_likes_comment", on_delete=models.CASCADE, null=True
    )
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment
   


class Reply(models.Model):

    reply_by = models.ForeignKey(
        User, related_name="reply_by", on_delete=models.CASCADE, null=True
    )
    related_comment = models.ForeignKey(
        Comment, related_name="post_comment_reply", on_delete=models.CASCADE
    )
    likes = models.ManyToManyField(User, blank=True, related_name="liked_replies", symmetrical=False)
    dislikes = models.ManyToManyField(User, blank=True, related_name="disliked_replies", symmetrical=False)
    body = models.CharField(max_length=300)
    timestamp = models.DateTimeField(auto_now_add=True)
    flagged = models.BooleanField(default=False)

    def upvote(self, user):
        self.likes.add(user)
        self.dislikes.remove(user)
        self.save()

    def downvote(self, user):
        self.likes.remove(user)
        self.dislikes.add(user)
        self.save()

    @property
    def vote_count(self):
        likes = self.likes.count()
        dislikes = self.dislikes.count()
        votes = likes - dislikes
        return votes
        
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

class ReplyLike(models.Model):
    reply = models.ForeignKey(
        Reply, related_name="reply_likes", on_delete=models.CASCADE
        )
    user = models.ForeignKey(
        User, related_name="user_likes_reply", on_delete=models.CASCADE, null=True
    )
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reply
 

class Repost(models.Model):
    reposted_by = models.ForeignKey(
        User, related_name="profile_repost", on_delete=models.CASCADE, null=True
    )
    post = models.ForeignKey(
        Post, related_name="post", on_delete=models.CASCADE, null=True
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

    def __str__(self):
        return self.original_post

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ["-timestamp"]
        
    def __str__(self):
        return self.user

