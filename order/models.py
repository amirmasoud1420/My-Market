from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import *
from product.models import *
from customer.models import *
from .validators import *


# Create your models here.

class Order(BaseModel, TimestampMixin):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name=_('Customer'),
        help_text=_('customer for this order'),
    )
    off_code = models.ForeignKey(
        OffCode,
        on_delete=models.SET_NULL,
        verbose_name=_('Off Code'),
        help_text=_('Off code for this order'),
        null=True,
        blank=True,
    )
    status = models.CharField(
        choices=(
            ('d', 'during'),
            ('p', 'paid'),
            ('c', 'canceled'),
        ),
        default='d',
        verbose_name=_('Status'),
        help_text=_('Status for this order'),
        max_length=10,
    )
    menu_item_variants = models.ManyToManyField(
        MenuItemVariant,
        through="OrderMenuItem",
        through_fields=(
            'order',
            'menu_item_variant',
        ),
    )
    paid_price = models.IntegerField(
        verbose_name=_('Paid Price'),
        null=True,
        blank=True,
    )

    def pure_price(self):
        price = 0
        for i in self.ordermenuitem_set.all():
            price += (i.menu_item_variant.final_price() * i.quantity)
        return price

    def final_price(self):
        price = self.pure_price()
        if self.off_code:
            final_price = self.off_code.final_price(price)
            return final_price
        else:
            return price

    def __str__(self):
        return f"{self.id}# {self.customer.user.phone} : {self.status} : {self.final_price()}"

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')


class OrderMenuItem(BaseModel, TimestampMixin):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name=_('Order'),
        help_text=_('order'),
    )
    menu_item_variant = models.ForeignKey(
        MenuItemVariant,
        on_delete=models.CASCADE,
        verbose_name=_('Menu Item'),
        help_text=_('menu item'),
    )
    quantity = models.IntegerField(
        verbose_name=_('Quantity'),
        help_text=_('quantity'),
        validators=[quantity_validator]
    )

    def final_price(self):
        return self.menu_item_variant.final_price() * self.quantity

    def __str__(self):
        return f"{self.id}# {self.order}: {self.menu_item_variant} : {self.quantity}"

    class Meta:
        verbose_name = _('OrderMenuItem')
        verbose_name_plural = _('OrderMenuItems')
