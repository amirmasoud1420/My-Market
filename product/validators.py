from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


def percent_validator(value):
    if value < 0 or value > 100:
        raise ValidationError(_('discount is percent and between 0 , 100'))


def price_validator(value):
    if value < 0:
        raise ValidationError(_('Price can not be negative'))
