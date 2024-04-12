from decimal import Decimal
from django.db.models.signals import post_save
from django.dispatch import receiver
from posts.models import View
from .models import Wallet
from django.contrib.auth.signals import user_logged_in

@receiver(post_save, sender=View)
def increment_wallet_total_earn(sender, instance, created, **kwargs):
    if created:  # Check if a new view object is created
        post_author = instance.post.posted_by  # Get the author of the post
        post_author_wallet = Wallet.objects.get(owner=post_author)
        # Increment total_earn by Decimal('0.2')
        post_author_wallet.total_earn += Decimal('0.2')
        post_author_wallet.balance += Decimal('0.2')

        post_author_wallet.save()

@receiver(user_logged_in)
def create_wallet(sender, user, request, **kwargs):
    if not hasattr(user, 'wallet'):
        # Create a wallet for the user if it doesn't exist
        Wallet.objects.create(owner=user)