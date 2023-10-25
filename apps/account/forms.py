from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.core.exceptions import ValidationError

from .models import User


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2"
        )


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())

    

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            "image",
            "username",
            "first_name",
            "last_name",
        )

    def clean_username(self):
        username: str = self.cleaned_data.get("username")
        if username:
            if len(username) < 3:
                raise ValidationError("Too short username")
            elif not username.isalnum():
                raise ValidationError("Username can contain letters and numbers only")

        return username

    def clean_first_name(self):
        first_name: str = self.cleaned_data.get("first_name")
        if first_name:
            if len(first_name) < 2:
                raise ValidationError("Too short first name")
            elif not first_name.isalpha():
                raise ValidationError("Not allowed symbols")
        
        return first_name

    def clean_last_name(self):
        last_name: str = self.cleaned_data.get("last_name")
        if last_name:
            if len(last_name) < 2:
                raise ValidationError("Too short first name")
            elif not last_name.isalpha():
                raise ValidationError("Not allowed symbols")
        
        return last_name
    