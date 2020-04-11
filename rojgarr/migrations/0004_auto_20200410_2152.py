# Generated by Django 2.0.13 on 2020-04-10 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rojgarr', '0003_auto_20200410_1233'),
    ]

    operations = [
        migrations.AddField(
            model_name='register_company_detail',
            name='address_latitude',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=9),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='register_company_detail',
            name='address_longitude',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=9),
            preserve_default=False,
        ),
    ]
