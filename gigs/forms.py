from django import forms
from django.forms import ModelForm, TextInput, Textarea, SelectDateWidget, IntegerField, NumberInput
from .models import *


class GigForm(ModelForm):
    industry= forms.ChoiceField(choices=Industries.choices, label="Gig Industry")

    gig_type= forms.ChoiceField(choices=GigType.choices, label="GigType")
    experience= forms.ChoiceField(choices=Experience.choices, label="Experience")

    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'post-edit', 'placeholder': 'Headline'}),
        label=False
    )
    location = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'post-edit', 'placeholder': 'Location'}),
        label=True
    )
  
    body = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'profile-textarea', 'placeholder': 'Extra Details'}),
        label=False
    )
    apply_link = forms.URLField(
        widget=forms.URLInput(attrs={'class': 'profile-edit', 'placeholder': 'Application Link'}),
        label=False,
        required=False
    )
    class Meta:
        model = Gig    
        fields = ('title','body', 'gig_type', 'experience', 'apply_link',  'location')

class ApplyForm(ModelForm):
    
    body = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'profile-textarea', 'placeholder': 'Extra Details'}),
        label=False
    )
    class Meta:
        model = Apply    
        fields = ('body', )