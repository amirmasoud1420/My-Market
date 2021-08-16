# Generated by Django 3.2.5 on 2021-08-15 16:38

from django.db import migrations, models
import order.validators


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermenuitem',
            name='quantity',
            field=models.IntegerField(help_text='quantity', validators=[order.validators.quantity_validator], verbose_name='Quantity'),
        ),
    ]
