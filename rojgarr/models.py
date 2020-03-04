from django.db import models
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.
class Vacancy_Detail(models.Model):
    company_name = models.CharField(max_length=50)
    company_address = models.CharField( max_length=50)
    skill = models.CharField( max_length=50)
    salary = models.IntegerField()
    urgent = models.BooleanField(default=False)
    date_added = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.company_name

class Register_Detail(models.Model):
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    email_password = models.CharField(max_length=50)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email
    
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token_(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)
        
    

class Advertisement_Detail(models.Model):
    link = models.CharField(max_length=60)
    image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None)
    short_description = models.CharField(max_length= 200)
    