# Generated by Django 2.0.13 on 2020-04-10 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rojgarr', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register_company_detail',
            name='company_password',
            field=models.CharField(max_length=500),
        ),
    ]
