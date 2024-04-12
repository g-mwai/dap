from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from . import Post
from moderation.models import Report

@receiver(post_save, sender=Report)
def update_post_report_count_on_create(sender, instance, created, **kwargs):
    if created:
        instance.post.update_report_count()

@receiver(post_delete, sender=Report)
def update_post_report_count_on_delete(sender, instance, **kwargs):
    instance.post.update_report_count()
