from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL


class Access(models.TextChoices):
        OPEN = 'Open', "OPEN"
        RESTRICTED = 'Restricted', "RESTRICTED"


class Category(models.Model):
    name = models.CharField(max_length=100)


class Forum(models.Model):
    forum_name = models.CharField(max_length=100, unique=True)
    category = models.ManyToManyField(
        Category, blank=True, related_name="forum_category"
    )
    about = models.TextField(max_length=100)
    moderator = models.ForeignKey(
        User, related_name="forum_mod", on_delete=models.CASCADE, null=True
    )
    members = models.ManyToManyField(
        User, related_name="forum_members"
    )
    visibility = models.CharField(max_length=50,
        choices=Access.choices,
        default=Access.OPEN
        )
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return self.forum_name

class Guidelines(models.Model):
    rule = models.CharField(max_length=100)
    forum = models.ForeignKey(
        Forum, related_name="forum_rules", on_delete=models.CASCADE, null=True
    )
 