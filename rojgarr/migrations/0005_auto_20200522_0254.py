# Generated by Django 2.0.13 on 2020-05-21 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rojgarr', '0004_auto_20200522_0015'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='experience',
        ),
        migrations.AddField(
            model_name='profile',
            name='experience_year',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
