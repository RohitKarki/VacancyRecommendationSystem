# Generated by Django 2.0.13 on 2020-04-10 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rojgarr', '0002_auto_20200410_1216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register_detail',
            name='email_password',
            field=models.CharField(max_length=500),
        ),
    ]