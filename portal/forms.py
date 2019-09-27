from django import forms
from django.db.models.fields import BLANK_CHOICE_DASH
from django.urls import reverse
from .models import Team

class SubmitForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['presentation', 'submission']
