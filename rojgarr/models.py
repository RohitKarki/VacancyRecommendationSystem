from django.db import models
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from django.contrib.auth.models import(
    AbstractBaseUser, BaseUserManager 
)

# Create your models here.
#  create model after customoze the user
class UserManger(BaseUserManager):
    def create_user(self, email, password=None, is_active=True, is_admin=False, is_employer=False, is_employe=False, is_staff=False):
        if not email:
            raise ValueError("User must have an email address")
        if not password:
            raise ValueError("User must have a password")

        user_obj = self.model(
            email = self.normalize_email(email),
        )
        user_obj.set_password(password)
        user_obj.active = is_active
        user_obj.admin = is_admin
        user_obj.employer = is_employer
        user_obj.employe = is_employe 
        user_obj.staff = is_staff
        user_obj.save(using=self.db)
        return user_obj
    
    def create_employeruser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_employer = True
            
        )
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email, 
            password=password,
            is_staff = True,
            is_admin = True
        )
        return user
    def create_employeuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_employe = True
        )
        return user

    def create_staffuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_staff = True
        )
        return user    

class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique = True)
    active = models.BooleanField(default=True) # can log in
    admin = models.BooleanField(default=False)# admin super user
    staff = models.BooleanField(default=False) # staff user
    employer = models.BooleanField(default=False) # emloyer user
    employe = models.BooleanField(default=False) # employe user
    timstamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    #  email and password are required by default
    REQUIRED_FIELDS = []

    objects = UserManger()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email
    
    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
        
    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail( subject, message, from_email, [self.email], **kwargs)

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_staff(self):
        return self.staff
    
    @property
    def id_employer(self):
        return self.employer

    @property
    def is_employe(self):
        return self.employe
    @property
    def is_active(self):
        return self.active

# model class for Register_Company_Detail
class Register_Company_Detail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank = False, null = False)
    company_name = models.CharField(max_length=100)
    company_address = models.CharField( max_length=50)
    company_contact = models.CharField( max_length=15)
    company_bussiness = models.CharField(max_length=255)
    address_latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    address_longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    
    def __str__(self):
        return self.company_name

@receiver(post_save, sender=User.employer)
def update_company_detail(sender, instance, created, **kwargs):
    if instance.employer:
        if created:
            Register_Company_Detail.objects.create(user=instance)
        instance.register_company_detail.save()

# @receiver(post_save, sender=User.employer) 
# def save_profile(sender, instance, **kwargs):
# 	instance.register_company_detail.save()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank = True, null = True)
    full_name = models.CharField(max_length=100)
    permanent_address = models.CharField( max_length=50)
    temporary_address = models.CharField( max_length=50)
    contact = models.CharField( max_length=15)
    profession = models.CharField(max_length=100,null = False)
    education = models.CharField(max_length=100, null = False)
    experience_year = models.IntegerField(null=True, blank=False)
    skills = models.TextField(max_length=200,null = True)
    location_to_search_job = models.CharField( max_length=50, null = False)
    address_latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    address_longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    recommendation = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name

@receiver(post_save, sender=User)
def update_profile(sender, instance, created, **kwargs):
    if instance.employe:
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

# @receiver(post_save, sender=User)
# def update_company_user_detail(sender, instance, created, **kwargs):
#     if instance.employer:
#         if created:
#             Register_Company_Detail.objects.create(user=instance)
#         instance.c_profile.save()

# model class for Vacancy_Detail
class Vacancy_Detail(models.Model):
    company = models.ForeignKey(Register_Company_Detail, on_delete=models.CASCADE, blank = False, null = False)
    job_category = models.CharField(max_length=50)
    job_title = models.CharField(max_length=50)
    education = models.CharField(max_length=100, null = False)
    work_type = models.CharField(max_length=20)
    payment_type = models.CharField(max_length=50)
    range_of_salary = models.IntegerField(null=True, blank=True)
    plus_services = models.CharField( max_length=200)
    experience_year = models.IntegerField(null=False, blank=False)
    task_and_responsibilities = models.TextField(max_length=200)
    qualification_and_experience = models.TextField(max_length=300)
    expiry_date = models.DateTimeField()
    date_added = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.job_title

# model class for company_review
class Company_Review(models.Model):
    email = models.ForeignKey(Profile, on_delete=models.CASCADE, blank = True, null = True)
    company_name = models.CharField(max_length=50)
    job_title = models.CharField(max_length=50)
    oppurtunity_rate = models.CharField(max_length=50)
    working_environment = models.CharField(max_length=20)
    management = models.CharField(max_length=20)
    benefits_perks = models.CharField(max_length=20)
    facilities = models.CharField(max_length=20)
    recommend_other = models.BooleanField()
    salary_rate = models.CharField(max_length=20)
    good_things = models.TextField(max_length=200)
    challeneges = models.TextField(max_length=200)
    company_summary = models.TextField(max_length=200)

# models class for add advertisement
class Advertisement_Detail(models.Model):
    advertiser_name = models.CharField(max_length=50)
    link = models.CharField(max_length=60)
    image = models.ImageField(upload_to='pics', height_field=None, width_field=None, max_length=None)
    short_description = models.CharField(max_length= 200)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.advertiser_name

    # else:
    #     raise ValueError("Signal problem.")
# model class for Register_Detail of normal user
# class Register_Detail(models.Model):  
#     full_name = models.CharField(max_length=50)
#     email = models.EmailField(max_length=254)
#     email_password = models.CharField(max_length=500)
#     date_added = models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return self.email
    
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token_(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)
        
    
# model class for Advertisement_Detail

