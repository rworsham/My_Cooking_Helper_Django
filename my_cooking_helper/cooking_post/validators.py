from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def validate_email_does_not_exist(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError(f'The email "{value}" is already in use.')