# Generated by Django 3.2.5 on 2021-08-11 08:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delete_time_stamp', models.DateTimeField(blank=True, default=None, help_text='Time of delete', null=True, verbose_name='Deleted Time Stamp')),
                ('is_deleted', models.BooleanField(default=False, help_text='Is delete or not?', verbose_name='Is Deleted')),
                ('create_time_stamp', models.DateTimeField(auto_now_add=True, help_text='Time of create', verbose_name='Create Time Stamp')),
                ('modify_time_stamp', models.DateTimeField(auto_now=True, help_text='Time of modify', verbose_name='Modify Time Stamp')),
                ('image', models.FileField(blank=True, help_text='customer image', null=True, upload_to='customer/customer/images/', verbose_name='Customer image')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delete_time_stamp', models.DateTimeField(blank=True, default=None, help_text='Time of delete', null=True, verbose_name='Deleted Time Stamp')),
                ('is_deleted', models.BooleanField(default=False, help_text='Is delete or not?', verbose_name='Is Deleted')),
                ('create_time_stamp', models.DateTimeField(auto_now_add=True, help_text='Time of create', verbose_name='Create Time Stamp')),
                ('modify_time_stamp', models.DateTimeField(auto_now=True, help_text='Time of modify', verbose_name='Modify Time Stamp')),
                ('State', models.CharField(help_text='The State', max_length=50, verbose_name='The State')),
                ('city', models.CharField(help_text='The City', max_length=50, verbose_name='The City')),
                ('postal_code', models.CharField(help_text='The Postal code', max_length=10, verbose_name='The Postal code')),
                ('detail', models.TextField(help_text='detail', verbose_name='Detail')),
                ('lat', models.FloatField(help_text='latitude', verbose_name='Latitude')),
                ('lng', models.FloatField(help_text='longitude', verbose_name='Longitude')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
