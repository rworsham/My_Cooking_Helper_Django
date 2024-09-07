from django import forms
from django.core.validators import EmailValidator
from django_recaptcha.fields import ReCaptchaField

class ContactForm(forms.Form):
    name = forms.CharField(
        label="Name",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    contact_reason = forms.ChoiceField(
        label="Subject",
        choices=[
            ("Quote", "Quote"),
            ("Information Request", "Information Request"),
            ("Other", "Other")
        ],
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label="Email",
        required=True,
        validators=[EmailValidator()],
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        label="Phone Number",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    message = forms.CharField(
        label="Message",
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 6})
    )
    recaptcha = ReCaptchaField(
        label="",
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data