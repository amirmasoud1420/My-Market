# Generated by Django 3.2.5 on 2021-07-31 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False, help_text='Is delete or not?', verbose_name='Is Deleted')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
