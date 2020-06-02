# Generated by Django 2.0.13 on 2020-05-28 08:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('rojgarr', '0010_remove_advertisement_detail_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement_detail',
            name='date_added',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='advertisement_detail',
            name='image',
            field=models.ImageField(default=0, upload_to='pics'),
            preserve_default=False,
        ),
    ]
