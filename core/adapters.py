from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.urls import reverse
from .views import home

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_login_redirect_url(self, request):
        # Redirect the user to the 'home' URL after registration
        return reverse('home')
