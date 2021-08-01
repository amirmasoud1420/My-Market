from django.db import models

# Create your models here.
from django.utils.translation import gettext_lazy as _


class BaseManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    def archive(self):
        return super().get_queryset()


class BaseModel(models.Model):
    delete_time_stamp = models.DateTimeField(
        default=None,
        null=True,
        blank=True,
        verbose_name=_('Deleted Time Stamp'),
        help_text=_('Time of delete'),
    )
    is_deleted = models.BooleanField(
        verbose_name=_('Is Deleted'),
        default=False,
        help_text=_('Is delete or not?'),
    )

    indexes = [
        models.Index(fields=['is_deleted'])
    ]
    objects = BaseManager()

    def my_delete(self):
        from datetime import datetime
        self.delete_time_stamp = datetime.now()
        self.is_deleted = True
        self.save()

    class Meta:
        abstract = True


class TimestampMixin(models.Model):
    create_time_stamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Create Time Stamp'),
        help_text=_('Time of create'),
    )
    modify_time_stamp = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Modify Time Stamp'),
        help_text=_('Time of modify'),
    )

    class Meta:
        abstract = True


class TestModel(BaseModel, TimestampMixin):
    pass
