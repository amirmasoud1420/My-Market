from django.db import models

# Create your models here.
from django.utils.translation import gettext_lazy as _

from core.models import *


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
