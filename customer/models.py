from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import *


# Create your models here.
class Customer(BaseModel, TimestampMixin):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    image = models.FileField(
        verbose_name=_('Customer image'),
        help_text=_('customer image'),
        upload_to='customer/customer/images/',
        null=True,
        blank=True,
        default='customer/customer/images/default.jpg'
    )

    def my_delete(self):
        super().my_delete()
        self.user.is_active = False
        self.user.save()
        for i in self.address_set.all():
            i.delete_time_stamp = timezone.now()
            i.is_deleted = True
            i.save()

    def __str__(self):
        return f"{self.id}# {self.user.phone}"

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')


class Address(BaseModel, TimestampMixin):
    owner = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
    )
    state = models.CharField(
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

    def __str__(self):
        return f"{self.id}#{self.owner.user.phone} : {self.state}-{self.city}"

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')
