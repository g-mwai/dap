from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *
from django.forms import ModelForm, TextInput, EmailInput, PasswordInput, IntegerField, SelectDateWidget,  Textarea, URLField, URLInput
from datetime import datetime
User = get_user_model()

# Create your forms here.

class NewUserForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'validate', 'placeholder': 'Username'}),
        label=False
    )
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'validate', 'placeholder': 'Your Email'}),
        label=False
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'validate', 'placeholder': 'Password'}),
        label=False
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'validate', 'placeholder': 'Confirm Password'}),
        label=False
    )
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    
    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already in use. Please choose a different one.")
        return username

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username','password']
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
        self.fields['username'].label = False
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password'}) 
        self.fields['password'].label = False
        
class EditProfileForm(ModelForm):

    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'profile-edit', 'placeholder': 'Screen Name'}),
        label=False
    )
    job_title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'profile-edit', 'placeholder': 'Job Title'}),
        label=False
    )
 
    ext_link = forms.URLField(
        widget=forms.URLInput(attrs={'class': 'profile-edit', 'placeholder': 'Your URL Link'}),
        label=False,
        required=False
    )
    location = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'profile-edit', 'placeholder': 'Location'}),
        label=False
    )
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'post-input', 'placeholder': 'Your Bio'}),
        label=False
    )

    class Meta:
        model = Profile
        fields = ('name','job_title', 'ext_link', 'location', 'bio')



class EditAccountForm(ModelForm):
    industry= forms.ChoiceField(choices=Industries.choices, label="Industry")
    # profile_type= forms.ChoiceField(choices=ProfileType.choices, label="Profile Type")
    
    gender= forms.ChoiceField( choices=Gender.choices, label="Gender")

    # username = forms.CharField(
    #     widget=forms.TextInput(attrs={'class': 'profile-edit', 'placeholder': 'Username'}),
    #     label=False
    # )
    job_title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'profile-edit', 'placeholder': 'Job Title'}),
        label=False
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'profile-edit', 'placeholder': 'Screen Name'}),
        label=False
    )

    birthday = forms.DateField(widget=SelectDateWidget(years=range(1950, datetime.now().year + 1)))
    ext_link = forms.CharField(
        widget=forms.URLInput(attrs={'class': 'profile-edit', 'placeholder': 'URL:  https://yourlink.com'}),
        label=False,
        required = False
    )
    location = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'profile-edit', 'placeholder': 'City'}),
        label=False
    )
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'profile-textarea', 'placeholder': 'Your Bio'}),
        label=False
    )

    class Meta:
        model = Profile
        fields = ( 'name', 'job_title', 'gender', 'industry', 'country', 'location', 'birthday', 'ext_link',  'bio')

    # def __init__(self, *args, **kwargs):
    #     super(EditAccountForm, self).__init__(*args, **kwargs)
    #     self.fields['username'].initial = self.instance.user.username

    # def clean_username(self):
    #     username = self.cleaned_data['username']
    #     user = User.objects.exclude(pk=self.instance.user.pk).filter(username=username)
    #     if user.exists():
    #         raise forms.ValidationError("Username is already taken.")
    #     return username

class ConfirmPassword(ModelForm):
    class Meta:
        model = User
        fields = ('password',)


class EditUsernameForm(forms.Form):
    new_username = forms.CharField(label='New Username', max_length=150)


class PasswordChangeForm(ModelForm):
    class Meta:
        model = PasswordChangeRequest    
        fields = ('user','code')