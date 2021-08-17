from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

# Create your models here.
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .validators import *


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
        self.delete_time_stamp = timezone.now()
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


class MyUserBaseManager(UserManager):

    def create(self, **kwargs):
        return super().create(username=kwargs['phone'], **kwargs)

    def create_superuser(self, username=None, email=None, password=None, **extra_fields):
        username = extra_fields['phone']
        return super().create_superuser(username, email, password, **extra_fields)

    def create_user(self, username=None, email=None, password=None, **extra_fields):
        username = extra_fields['phone']
        return super().create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    USERNAME_FIELD = 'phone'

    phone = models.CharField(
        verbose_name=_('Phone Number'),
        help_text=_('Phone Number'),
        unique=True,
        max_length=13,
        validators=[phone_validator],
    )
    objects = MyUserBaseManager()


class TestModel(BaseModel, TimestampMixin):
    pass
