from django import forms
from django.contrib.auth import get_user_model
from .models import *
from django.forms import ModelForm, TextInput, EmailInput, PasswordInput, IntegerField, SelectDateWidget,  Textarea, URLField, URLInput
from datetime import datetime
User = get_user_model()


class NewShopForm(ModelForm):
    industry= forms.ChoiceField(choices=Industries.choices, label="Industry")

    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'profile-edit', 'placeholder': 'Shop Name'}),
        label=False
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'profile-edit', 'placeholder': 'Username'}),
        label=False
    )
   
    ext_link = forms.URLField(
        widget=forms.URLInput(attrs={'class': 'profile-edit', 'placeholder': 'Website'}),
        label=False,
        required=False
    )
   
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'post-input', 'placeholder': 'Your Bio'}),
        label=False
    )

    class Meta:
        model = Shop
        fields = ('industry', 'name', 'username', 'ext_link', 'bio')


# class ServiceForm(ModelForm):

#     class Meta:
#         model = Service
#         fields = ('name','price_low', 'price_up' )


class LocationForm(ModelForm):

    class Meta:
        model = Location
        fields = ('name', )

