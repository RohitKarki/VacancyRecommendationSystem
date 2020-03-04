# Generated by Django 2.0.13 on 2020-01-21 12:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('rojgarr', '0002_vacancy_detail_salary'),
    ]

    operations = [
        migrations.CreateModel(
            name='Register_Detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('email_password', models.CharField(max_length=50)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]