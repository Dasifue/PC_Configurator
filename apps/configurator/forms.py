from django import forms

from .models import Configuration

class CreateConfigurationForm(forms.ModelForm):

    class Meta:
        model = Configuration
        fields = ("name", "main")