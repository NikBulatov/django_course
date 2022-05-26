import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_name(value):
    if value.isdigit():
        raise ValidationError(
            _(f"Имя не может быть только цифрами"), params={'value': value})
    if not value.isalpha():
        raise ValidationError(
            _(f"Имя не может содержать цифры"), params={'value': value})


def validate_email(value):
    if re.search(r'([A-Za-z\d+-_]+)@([A-Za-z]\.\w{2,3})', value):
        raise ValidationError(
            _(f'Введите валидный email (Например: example@mail.com'), params={'value': value})
