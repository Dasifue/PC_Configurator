from django import forms
from django.core.exceptions import ValidationError

from .models import Configuration

class ConfigurationForm(forms.ModelForm):

    class Meta:
        model = Configuration
        fields = ("name", "main")

    def clean_name(self):
        name: str = self.cleaned_data.get("name")
        if name.isspace():
            raise ValidationError("Wrong configuration name")
        return name

    def save(self, **kwargs):
        configuration = super().save(**kwargs)  
        configuration.main = self.cleaned_data.get("main")
        configuration.save()
        return configuration
    
    