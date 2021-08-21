# Generated by Django 3.2.5 on 2021-08-21 07:11

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20210820_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, help_text='Enter the menu item description', null=True, verbose_name='menu item description'),
        ),
    ]
