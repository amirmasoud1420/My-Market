import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


def percent_validator(value):
    if value < 0 or value > 100:
        raise ValidationError(_('discount is percent and between 0 , 100'))


def price_validator(value):
    if value < 0:
        raise ValidationError(_('Price can not be negative'))


def off_code_validator(value):
    pattern = r"([a-zA-Z0-9]){5,14}"
    x = re.search(pattern, value)
    if x:
        if x.group() != value:
            raise ValidationError(
                _('The code is invalid! Code can only contain letters and numbers and be between 5 and 14 characters'))
    else:
        raise ValidationError(
            _('The code is invalid! Code can only contain letters and numbers and be between 5 and 14 characters'))


def menu_item_name_validator(value):
    pattern = r"([a-zA-Z0-9]){1,30}"
    x = re.search(pattern, value)
    if x:
        if x.group() != value:
            raise ValidationError(
                _('The menu item name is invalid!'))
    else:
        raise ValidationError(
            _('The menu item name is invalid!'))


def rate_validator(value):
    if value < 1:
        raise ValidationError(_('Rate most be bigger than 1 '))
