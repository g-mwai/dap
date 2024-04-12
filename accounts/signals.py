from django.dispatch import receiver
from allauth.socialaccount.signals import pre_social_login
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from accounts.models import User

@receiver(pre_social_login)
def social_login_handler(sender, request, sociallogin, **kwargs):
    user = sociallogin.user
    
    # Check if a user with the same email already exists
    existing_user = User.objects.filter(email=user.email).first()
    if existing_user:
        # If a user with the same email exists, prompt the user to log in instead
        sociallogin.connect(request, existing_user)
        redirect_url = '/accounts/login/?google_login=1'  # Customize the login URL as needed
        return redirect(redirect_url)

    # If the user doesn't exist, derive a username from the email
    if not user.username:
        user.username = user.email.split('@')[0]  # Or use any other method to derive username
        user.save()
