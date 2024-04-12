from ast import Mod
from dataclasses import field
from django import forms
from .models import *
from django.forms import ModelForm

class NewForumForm(ModelForm):
    class Meta:
        model = Forum
        fields = ( 'forum_name', 'category', 'about',  'body')

class NewCategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ( 'name',)


class NewRuleForm(ModelForm):
    class Meta:
        model = Guidelines
        fields = ( 'rule',)


