from django.db import models
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.
class Register_Company_Detail(models.Model):
    company_name = models.CharField(max_length=50)
    company_address = models.CharField( max_length=50)
    company_contact = models.CharField(max_length=10)
    company_email = models.CharField( max_length=100 )
    company_password = models.CharField( max_length=500 )
    company_date_added = models.DateTimeField(default=timezone.now )
    address_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    address_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    
    def __str__(self):
        return self.company_name

# @receiver(post_save, sender=User)
# def company_user_created(sender, instance, created, **kwargs):
#         if created:
#             Register_Company_Detail.objects.create(company_user=instance)
#         else:
#             instance.Register_Company_Detail.save()

class Vacancy_Detail(models.Model):
    company = models.ForeignKey(Register_Company_Detail, on_delete=models.CASCADE, blank = True, null = True)
    job_category = models.CharField(max_length=50)
    job_title = models.CharField(max_length=50)
    work_type = models.CharField(max_length=20)
    payment_type = models.CharField(max_length=50)
    range_of_salary = models.IntegerField(null=True, blank=True)
    plus_services = models.CharField( max_length=200)
    task_and_responsibilities = models.TextField(max_length=200)
    qualification_and_experience = models.TextField(max_length=300)
    expiry_date = models.DateTimeField()
    date_added = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.job_title


class Register_Detail(models.Model):  
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    email_password = models.CharField(max_length=500)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email
    
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token_(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)
        
    

class Advertisement_Detail(models.Model):
    advertiser_name = models.CharField(max_length=50)
    link = models.CharField(max_length=60)
    image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None)
    short_description = models.CharField(max_length= 200)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.advertiser_name