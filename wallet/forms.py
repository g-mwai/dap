from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *
from django.forms import ModelForm, TextInput, EmailInput, PasswordInput, IntegerField, SelectDateWidget,  Textarea, URLField, URLInput
from datetime import datetime


class BetForm(ModelForm):
    class Meta:
        model = Bet    
        fields = ('amount',)