# Generated by Django 2.0.13 on 2020-01-11 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rojgarr', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy_detail',
            name='salary',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]