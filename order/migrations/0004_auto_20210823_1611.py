# Generated by Django 3.2.5 on 2021-08-23 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='paid_price',
            field=models.IntegerField(blank=True, null=True, verbose_name='Paid Price'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('d', 'during'), ('p', 'paid'), ('c', 'canceled')], default='d', help_text='Status for this order', max_length=10, verbose_name='Status'),
        ),
    ]
