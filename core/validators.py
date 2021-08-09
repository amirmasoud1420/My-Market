import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


def phone_validator(value):
    pattern = r"(\+98([0-9]){10})"
    x = re.search(pattern, value)
    if x:
        if x.group() != value:
            raise ValidationError(_('Invalid phone number'))
    else:
        raise ValidationError(_('Invalid phone number'))
