from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import *
from .validators import *
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from django.db.models import Avg, Min, Max
from customer.models import *


# Create your models here.


class Category(BaseModel, TimestampMixin):
    name = models.CharField(
        max_length=50,
        verbose_name=_('Name'),
        help_text=_('Category Name'),
    )
    name_fa = models.CharField(
        max_length=50,
        verbose_name=_('PersianName'),
        null=True,
        blank=True,
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    is_sub_category = models.BooleanField(
        verbose_name=_('Is sub category?'),
        help_text=_('Is sub category? or main?'),
        default=False,
    )

    def my_delete(self):
        super().my_delete()
        for i in self.category_set.all():
            i.my_delete()

    def __str__(self):
        return f"{self.id}# {self.name}"

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


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

    def __str__(self):
        if self.is_percent:
            return f"{self.id}# {self.percent}% , max = {self.max} , expire-date = {self.expire_date_time} , {self.is_expired()}"
        else:
            return f"{self.id}# {self.price}$ , max = {self.max} , expire-date = {self.expire_date_time} , {self.is_expired()}"

    class Meta:
        verbose_name = _('Discount')
        verbose_name_plural = _('Discounts')


class OffCode(Discount):
    code = models.CharField(
        verbose_name=_('Off Code'),
        max_length=14,
        validators=[off_code_validator],
        help_text=_('Enter the off code'),
    )

    class Meta:
        verbose_name = _('OffCode')
        verbose_name_plural = _('OffCodes')


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
    name_fa = models.CharField(
        max_length=50,
        verbose_name=_('PersianName'),
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')


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

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')


class Specification(BaseModel, TimestampMixin):
    name = models.CharField(
        max_length=200,
        verbose_name=_('Specification name'),
        help_text=_('Enter the Specification name'),
    )
    name_fa = models.CharField(
        max_length=200,
        verbose_name=_('PersianName'),
        null=True,
        blank=True,
    )
    value = models.CharField(
        max_length=200,
        verbose_name=_('Specification Value'),
        help_text=_('Enter the Specification value'),
    )
    value_fa = models.CharField(
        max_length=200,
        verbose_name=_('PersianValue'),
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.id}# {self.name} : {self.value}"

    class Meta:
        verbose_name = _('Specification')
        verbose_name_plural = _('Specifications')


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

    class Meta:
        verbose_name = _('VariableSpecification')
        verbose_name_plural = _('VariableSpecifications')


class MenuItem(BaseModel, TimestampMixin):
    name = models.CharField(
        max_length=50,
        verbose_name=_('menu item name'),
        help_text=_('Enter the Menu items name'),

    )
    name_fa = models.CharField(
        max_length=50,
        verbose_name=_('PersianName'),
        null=True,
        blank=True,
    )
    category = models.ManyToManyField(
        Category,
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
    description = RichTextUploadingField(
        verbose_name=_('menu item description'),
        help_text=_('Enter the menu item description'),
        null=True,
        blank=True,
    )
    description_fa = RichTextUploadingField(
        verbose_name=_('PersianDescription'),
        null=True,
        blank=True,
    )

    status = models.BooleanField(
        verbose_name=_('variant status'),
        help_text=_('has variant?'),
        default=False,
    )
    variable_specification_name = models.CharField(
        verbose_name=_('Variable Specification name'),
        help_text=_('variable specification name'),
        max_length=50,
        null=True,
        blank=True,
    )
    variable_specification_name_fa = models.CharField(
        verbose_name=_('Variable Specification persian name'),
        max_length=50,
        null=True,
        blank=True,
    )
    tags = TaggableManager(
        verbose_name=_('Similar specification'),
        help_text=_('for similar product'),
        blank=True,
    )
    favorites_customers = models.ManyToManyField(
        Customer,
        blank=True,
        related_name='favorites',
    )
    sell = models.IntegerField(default=0, verbose_name=_('sell count'))

    def my_delete(self):
        super().my_delete()
        for i in self.menuitemvariant_set.all():
            i.delete_time_stamp = timezone.now()
            i.is_deleted = True
            i.save()
        for i in self.comment_set.all():
            i.delete_time_stamp = timezone.now()
            i.is_deleted = True
            i.save()

    def average_rate(self):
        data = Comment.objects.filter(is_reply=False, menu_item=self).aggregate(avg=Avg('rate'))
        rate = 0
        if data['avg']:
            rate = round(data['avg'], 1)
        return rate

    def __str__(self):
        return f"{self.id}#   {self.name} "

    class Meta:
        verbose_name = _('MenuItem')
        verbose_name_plural = _('MenuItems')


class MenuItemVariant(BaseModel, TimestampMixin):
    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE,
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
    variable_specification_value = models.CharField(
        verbose_name=_('Variable Specification Value'),
        help_text=_('variable specification value'),
        max_length=50,
        default=_('Not entered'),
    )
    variable_specification_value_fa = models.CharField(
        verbose_name=_('Variable Specification persian Value'),
        max_length=50,
        null=True,
        blank=True,
    )
    likes = models.ManyToManyField(
        User,
        blank=True,
        verbose_name=_('Likes'),
        related_name='menu_item_variants_likes',
    )
    un_likes = models.ManyToManyField(
        User,
        blank=True,
        verbose_name=_('DisLikes'),
        related_name='menu_item_variants_un_likes',
    )

    def brand(self):
        return self.menu_item.brand

    def total_likes(self):
        return self.likes.count()

    def total_un_likes(self):
        return self.un_likes.count()

    def final_price(self):
        if self.discount:
            if self.discount.is_expired():
                return self.price
            return self.discount.final_price(self.price)
        else:
            return self.price

    def __str__(self):
        return f"{self.id}#   {self.menu_item.name} : {self.price} ------> final price = {self.final_price()}"

    class Meta:
        verbose_name = _('MenuItemVariant')
        verbose_name_plural = _('MenuItemsVariants')


class Comment(BaseModel, TimestampMixin):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
    )
    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE,
        verbose_name=_('Product'),
    )
    comment = models.TextField(
        verbose_name=_('Comment')
    )
    rate = models.PositiveIntegerField(default=1)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='comment_childes',
    )
    is_reply = models.BooleanField(
        verbose_name=_('is reply?'),
        default=False,
    )
    likes = models.ManyToManyField(
        User,
        blank=True,
        verbose_name=_('Likes'),
        related_name='comments_likes',
    )
    un_likes = models.ManyToManyField(
        User,
        blank=True,
        verbose_name=_('Un Likes'),
        related_name='comments_un_likes',
    )

    def total_likes(self):
        return self.likes.count()

    def total_un_likes(self):
        return self.un_likes.count()

    def my_delete(self):
        super().my_delete()
        for i in self.comment_childes.all():
            i.my_delete()

    def __str__(self):
        return f"{self.id}# {self.user.phone} : {self.menu_item.name}"

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')


class Gallery(models.Model):
    name = models.CharField(
        verbose_name=_('image name'),
        max_length=50,
        blank=True,
        null=True,
    )
    name_fa = models.CharField(
        verbose_name=_('image persian name'),
        max_length=50,
        blank=True,
        null=True,
    )
    description = models.CharField(
        verbose_name=_('description'),
        max_length=300,
        blank=True,
        null=True,
    )
    description_fa = models.CharField(
        verbose_name=_('Persian description'),
        max_length=300,
        blank=True,
        null=True,
    )
    image = models.FileField(
        verbose_name=_('image'),
        upload_to='gallery/',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('Image Gallery')
        verbose_name_plural = _('Image Galleries')
