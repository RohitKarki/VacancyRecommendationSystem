# Generated by Django 2.0.13 on 2020-05-22 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rojgarr', '0005_auto_20200522_0254'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy_detail',
            name='education',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]
