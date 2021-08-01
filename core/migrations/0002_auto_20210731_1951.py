# Generated by Django 3.2.5 on 2021-07-31 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='testmodel',
            name='create_time_stamp',
            field=models.DateTimeField(auto_now_add=True, default='2021-01-01', help_text='Time of create', verbose_name='Create Time Stamp'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='testmodel',
            name='delete_time_stamp',
            field=models.DateTimeField(blank=True, default=None, help_text='Time of delete', null=True, verbose_name='Deleted Time Stamp'),
        ),
        migrations.AddField(
            model_name='testmodel',
            name='modify_time_stamp',
            field=models.DateTimeField(auto_now=True, help_text='Time of modify', verbose_name='Modify Time Stamp'),
        ),
    ]
