# Generated by Django 3.2.5 on 2021-08-25 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_menuitem_sell'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='image name')),
                ('description', models.CharField(blank=True, max_length=300, null=True, verbose_name='description')),
                ('image', models.FileField(blank=True, null=True, upload_to='gallery/', verbose_name='image')),
            ],
        ),
    ]
