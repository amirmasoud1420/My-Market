from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import *


# Create your models here.
class Customer(BaseModel, TimestampMixin):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )


class Address(BaseModel, TimestampMixin):
    owner = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
    )
    State = models.CharField(
        verbose_name=_("The State"),
        help_text=_("The State"),
        max_length=50,
    )
    city = models.CharField(
        verbose_name=_("The City"),
        help_text=_("The City"),
        max_length=50,
    )
    postal_code = models.CharField(
        verbose_name=_("The Postal code"),
        help_text=_("The Postal code"),
        max_length=10,
    )
    detail = models.TextField(
        verbose_name=_("Detail"),
        help_text=_("detail"),
    )
    lat = models.FloatField(
        verbose_name=_("Latitude"),
        help_text=_("latitude"),
    )
    lng = models.FloatField(
        verbose_name=_("Longitude"),
        help_text=_("longitude"),
    )
