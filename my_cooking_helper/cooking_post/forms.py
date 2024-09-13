from django import forms
from django.forms import ModelForm
from .validators import validate_email_does_not_exist
from django.core.validators import EmailValidator
from django_recaptcha.fields import ReCaptchaField


class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}), required=True)
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), required=True)

class SignUpForm(forms.Form):
    name = forms.CharField(
        label="Name",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label="Email",
        required=True,
        validators=[EmailValidator(), validate_email_does_not_exist],
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="Password",
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'})
    )
    recaptcha = ReCaptchaField(
        label="",
        required=True
    )
