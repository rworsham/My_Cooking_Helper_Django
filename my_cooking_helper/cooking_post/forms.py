from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}), required=True)
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), required=True)
