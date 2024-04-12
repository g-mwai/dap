from ast import Mod
from dataclasses import field
from django import forms
from .models import *
from django.forms import ModelForm, TextInput, Textarea, SelectDateWidget
from datetime import datetime

class PostForm(forms.ModelForm):
    industry= forms.ChoiceField(choices=Industries.choices, label="Industry")

    class Meta:
        model = Post
        fields = ('industry', 'body')

class SellForm(forms.ModelForm):

    cta= forms.ChoiceField(choices=CTA.choices, label="CTA")
    post_type= forms.ChoiceField(choices=PostType.choices, label="PostType")
    sell_type= forms.ChoiceField(choices=SellType.choices, label="SellType")

    headline = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'post-edit', 'placeholder': 'Headline'}),
        label=False
    )
    # closing_date = forms.DateField(widget=SelectDateWidget(years=range(datetime.now().year, datetime.now().year + 5)))
    # cta_link = forms.URLField(
    #     widget=forms.URLInput(attrs={'class': 'profile-edit', 'placeholder': 'Your URL Link'}),
    #     label=False,
    #     required=False
    # )
    class Meta:
        model = Post
        fields = ( 'headline', 'body', 'cta','sell_type', 'post_type', 'min_price', 'max_price')

class ProjectForm(forms.ModelForm):

    project_cta= forms.ChoiceField(choices=ProjectCTA.choices, label="ProjectCTA")
    industry= forms.ChoiceField(choices=Industries.choices, label="Industry")
    progress= forms.ChoiceField(choices=Progress.choices, label="Progress")

    headline = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'post-edit', 'placeholder': 'Headline'}),
        label=False
    )
    cta_link = forms.URLField(
        widget=forms.URLInput(attrs={'class': 'profile-edit', 'placeholder': 'Website Link'}),
        label=False,
        required=False
    )
    class Meta:
        model = Post
        fields = ( 'headline', 'progress', 'body', 'project_cta', 'industry', 'cta_link')


class YesNoForm(forms.ModelForm):
    closing_date = forms.DateField(widget=SelectDateWidget(years=range(datetime.now().year, datetime.now().year + 5)))
    headline = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'post-edit', 'placeholder': 'Question or Statement'}),
        label=False
    )

    class Meta:
        model = Post
        fields = ( 'body', 'headline', 'closing_date')

class PollForm(forms.ModelForm):
    closing_date = forms.DateField(widget=SelectDateWidget(years=range(datetime.now().year, datetime.now().year + 5)))
    headline = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'post-edit', 'placeholder': 'Question or Statement'}),
        label=False
    )


    class Meta:
        model = Post
        fields = ( 'body', 'headline', 'closing_date')

class OptionForm(ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'post-edit', 'placeholder': 'Name'}),
        label=False
    )
    class Meta:
        model = Option
        fields = ('name', )



class NewCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )


class NewReplyForm(ModelForm):
    class Meta:
        model = Reply
        fields = ('body', )

class NewTagForm(ModelForm):
    industry= forms.ChoiceField(choices=Industries.choices, label="Industry")

    class Meta:
        model = Tag
        fields = ('name','industry' )


class NewArticleForm(ModelForm):
    industry= forms.ChoiceField(choices=Industries.choices, label="Industry")

    class Meta:
        model = Post
        fields = ('industry','body', 'headline', 'tags' )




class BookmarkForm(forms.Form):
    post_id = forms.IntegerField()