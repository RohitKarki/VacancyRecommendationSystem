# Generated by Django 2.0.13 on 2020-01-21 12:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('rojgarr', '0003_register_detail'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy_detail',
            name='date_added',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
