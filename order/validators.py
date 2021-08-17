from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


def quantity_validator(value):
    if value <= 0:
        raise ValidationError(_('Invalid quantity! quantity must be greater than Zero.'))
