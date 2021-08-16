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
        return f"{self.id}# {self.name}"


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
    expire_date_time = models.DateTimeField(
        verbose_name=_('Expire Date'),
        help_text=_('Enter the expire date'),
    )

    def is_expired(self):
        if self.is_deleted:
            return True
        if timezone.now() > self.expire_date_time:
            return True
        return False

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
                return 0
                # raise AssertionError(_('discount price is bigger than product price'))

    def __str__(self):
        if self.is_percent:
            return f"{self.id}# {self.percent}% , max = {self.max} , expire-date = {self.expire_date_time} , {self.is_expired()}"
        else:
            return f"{self.id}# {self.price}$ , max = {self.max} , expire-date = {self.expire_date_time} , {self.is_expired()}"


class OffCode(Discount):
    code = models.CharField(
        verbose_name=_('Off Code'),
        max_length=14,
        validators=[off_code_validator],
        help_text=_('Enter the off code'),
    )


""""
    menu item classes
"""


class Brand(BaseModel, TimestampMixin):
    name = models.CharField(
        max_length=30,
        verbose_name=_('brand name'),
        help_text=_('Enter the brand name'),
        # validators=[menu_item_name_validator],
    )

    def __str__(self):
        return f"{self.id}# {self.name}"


class Image(BaseModel, TimestampMixin):
    image = models.FileField(
        verbose_name=_('menu item image'),
        help_text=_('Enter your image'),
        upload_to='product/menu_items/images/',
    )
    menu_item = models.ForeignKey(
        'MenuItem',
        on_delete=models.CASCADE,
        verbose_name=_('menu item for this image'),
        help_text=_('Enter the menu item for this image'),
    )


class Specification(BaseModel, TimestampMixin):
    name = models.CharField(
        max_length=200,
        verbose_name=_('Specification name'),
        help_text=_('Enter the Specification name'),
    )
    value = models.CharField(
        max_length=200,
        verbose_name=_('Specification Value'),
        help_text=_('Enter the Specification value'),
    )

    def __str__(self):
        return f"{self.id}# {self.name} : {self.value}"


class VariableSpecification(BaseModel, TimestampMixin):
    name = models.CharField(
        max_length=200,
        verbose_name=_('Specification name'),
        help_text=_('Enter the Specification name'),
    )
    value = models.CharField(
        max_length=200,
        verbose_name=_('Specification Value'),
        help_text=_('Enter the Specification value'),
    )

    def __str__(self):
        return f"{self.id}# {self.name} : {self.value}"


class MenuItem(BaseModel, TimestampMixin):
    name = models.CharField(
        max_length=30,
        verbose_name=_('menu item name'),
        help_text=_('Enter the Menu items name'),
        # validators=[menu_item_name_validator],
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name=_('menu item category'),
        help_text=_('Choose the menu item stock'),
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('menu item brand'),
        help_text=_('Choose the menu item brand'),
    )
    specifications = models.ManyToManyField(
        Specification,
        related_name='menu_items',
    )
    description = models.TextField(
        verbose_name=_('menu item description'),
        help_text=_('Enter the menu item description'),
        null=True,
        blank=True,
    )

    # variants = models.ManyToManyField(
    #     VariableSpecification,
    #     through="MenuItemVariant",
    #     through_fields=('menu_item', 'variable_specifications'),
    #     related_name="variants",
    # )

    def my_delete(self):
        super().my_delete()
        for i in self.menuitemvariant_set.all():
            i.delete_time_stamp = timezone.now()
            i.is_deleted = True
            i.save()

    def __str__(self):
        return f"{self.id}#  {self.category.name} > {self.name} "


class MenuItemVariant(BaseModel, TimestampMixin):
    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE,
    )
    variable_specifications = models.ManyToManyField(
        VariableSpecification,
        related_name='menu_item_variants',
    )
    price = models.IntegerField(
        verbose_name=_('menu item price'),
        help_text=_('Enter the menu item price'),
        validators=[price_validator],
    )
    count = models.IntegerField(
        verbose_name=_('menu item stock'),
        help_text=_('Enter the menu item stock'),
        validators=[price_validator],
        default=0,
    )
    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('menu item discount'),
        help_text=_('Enter the menu item discount'),
    )

    def final_price(self):
        if self.discount:
            if self.discount.is_expired():
                return self.price
            return self.discount.final_price(self.price)
        else:
            return self.price

    def __str__(self):
        return f"{self.id}#  {self.menu_item.category.name} > {self.menu_item.name} : {self.price} ------> final price = {self.final_price()}"
