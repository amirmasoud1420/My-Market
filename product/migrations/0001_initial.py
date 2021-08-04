# Generated by Django 3.2.5 on 2021-08-01 07:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delete_time_stamp', models.DateTimeField(blank=True, default=None, help_text='Time of delete', null=True, verbose_name='Deleted Time Stamp')),
                ('is_deleted', models.BooleanField(default=False, help_text='Is delete or not?', verbose_name='Is Deleted')),
                ('create_time_stamp', models.DateTimeField(auto_now_add=True, help_text='Time of create', verbose_name='Create Time Stamp')),
                ('modify_time_stamp', models.DateTimeField(auto_now=True, help_text='Time of modify', verbose_name='Modify Time Stamp')),
                ('name', models.CharField(help_text='Category Name', max_length=50, verbose_name='Name')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.category')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]