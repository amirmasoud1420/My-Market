from django.db import models

# Create your models here.
from django.utils.translation import gettext_lazy as _

from core.models import *
from .validators import *


class Category(BaseModel, TimestampMixin):
    name = models.CharField(
        max_length=50,
        verbose_name=_('Name'),
        help_text=_('Category Name'),
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def my_delete(self):
        super().my_delete()
        for i in self.category_set.all():
            i.my_delete()

    def __str__(self):
        return f"{self.name}"


class Discount(BaseModel, TimestampMixin):
    is_percent = models.BooleanField(
        default=False,
        verbose_name=_('Is Percent?'),
        help_text=_('Do you want to enter a percentage?'),
    )
    price = models.IntegerField(
        verbose_name=_('Discount Price'),
        help_text=_('Enter the discount price'),
        validators=[price_validator],
        default=0,
    )
    percent = models.FloatField(
        verbose_name=_('Discount Percent'),
        help_text=_('Enter the discount percent'),
        validators=[percent_validator],
        default=0,
    )
    max = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_('Max Discount Price'),
        help_text=_('Enter the max discount price'),
        validators=[price_validator],
    )

    def is_expired(self):
        return self.is_deleted

    def final_price(self, price):
        if self.is_percent:
            discount = (price * self.percent) // 100
            if self.max:
                if discount > self.max:
                    return price - self.max
                else:
                    return price - discount
            else:
                return price - discount
        else:
            if price > self.price:
                return price - self.price
            else:
                raise AssertionError(_('discount price is bigger than product price'))

