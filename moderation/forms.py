# forms.py
from django import forms
from .models import *
from ckeditor.widgets import CKEditorWidget  # Import CKEditorWidget from ckeditor.widgets

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['content']

class ReportGigForm(forms.ModelForm):
    class Meta:
        model = ReportGig
        fields = ['content']

class ReportCommentForm(forms.ModelForm):
    class Meta:
        model = ReportComment
        fields = ['content']

class ReportBugForm(forms.ModelForm):
    priority= forms.ChoiceField(choices=Priority.choices, label="Priority")

    class Meta:
        model = ReportBug
        fields = ('body', 'priority')

class NewPolicyForm(forms.ModelForm):
    pol= forms.ChoiceField(choices=Policies.choices, label="Policies")
    body = forms.CharField(
        widget=CKEditorWidget(config_name='default', attrs={'class': 'ckeditor'}),  # Use CKEditorWidget
        label=False
    )
    class Meta:
        model = Policy
        fields = ('pol', 'title', 'body' )
