from django import forms
from .models import *
from django.core.validators import validate_email
from django.shortcuts import redirect
from django.core.exceptions import ValidationError 
from django.contrib.auth import authenticate, get_user_model
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from phonenumber_field.formfields import PhoneNumberField
from geopy.geocoders import Nominatim
from math import *

User = get_user_model()

class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user



class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class RegisterEmployeForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-field','style': 'height: 10px; width:255px; margin: 10px; font-size: 15px','placeholder' : 'Password'}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class': 'form-field','style': 'height: 10px; width:255px; margin: 10px; font-size: 15px','placeholder' : 'Confirm password'}))
    full_name = forms.CharField(max_length=50,
    widget=forms.TextInput(attrs={'class': 'form-field','style': 'height: 10px; width:255px;margin: 10px;', 'placeholder' : 'Type Your Full Name'}), required = True)
    class Meta:
        model = User
        fields = ('full_name','email')
        widgets = {
            'full_name': forms.TextInput(
                attrs={'class': 'form-field','style': 'height: 10px; width:255px; margin: 10px; font-size: 15px','placeholder' : 'Type Your Full Name'}),
            'email': forms.EmailInput(
                 attrs={'class': 'form-field','style': 'height: 10px; width:255px; margin: 10px; font-size: 15px','placeholder' : 'Type Your Email'}),
        }

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterEmployeForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.employe = True
        user.active = False
        if commit:
            user.save()
        return user

class EditProfileForm(forms.ModelForm):
    full_name = forms.CharField(max_length=50,
    widget=forms.TextInput(attrs={'class': 'form-field','style': 'height: 10px; width:255px;margin: 10px;', 'placeholder' : 'Type Your Full Name'}), required = True)
    permanent_address = forms.CharField(max_length=50,
    widget=forms.TextInput(attrs={'class': 'form-field','style': 'height: 10px; width:255px;margin: 10px;', 'placeholder' : 'Type Your Permanent Address'}), required = False)
    temporary_address = forms.CharField(max_length=50,
    widget=forms.TextInput(attrs={'class': 'form-field','style': 'height: 10px; width:255px;margin: 10px;', 'placeholder' : 'Type Your Temporary Address'}), required = False)
    contact = forms.CharField(max_length=50,
    widget=forms.TextInput(attrs={'class': 'form-field','style': 'height: 10px; width:255px;margin: 10px;', 'placeholder' : 'Type Your Permanent Contact'}), required = False)
    available_catagories = [('None','None'),('Banking','Banking'),('Engineering','Engineering'),('Information Technology', 'Information Technology'),('Design and Architecture','Design and Architecture'),('Medical Sector','Medical Sector'), ('Marketing and Communications','Marketing and Communications'), ('Education and Training', 'Education and Training'), ('Sports', 'Sports'), ('Legal','Legal'),('Other','Other')]
    profession = forms.CharField(label='Job Catagory :', 
    widget=forms.Select(choices=available_catagories,attrs={'class': 'form-field','style':'height: 40px; width:290px;margin: 10px;'}), required = False)
    education_categories = [('None','None'),('Below SLC','Below SLC'),('SLC Passed','SLC Passed'),('+2 Passed','+2 Passed'),( 'Bachelor Passed','Bachelor Passed'),('Master Passed', 'Master Passed'), ('PHD Completed', 'PHD completed')]
    education = forms.CharField(label='Education Level :', 
    widget=forms.Select(choices=education_categories,attrs={'class': 'form-field','style':'height: 40px; width:290px;margin: 10px;'}), required = False)
    experience_year = forms.CharField(label='Expereience Approximate Year :',max_length=50,
    widget=forms.NumberInput(attrs={'class': 'form-field','style': 'height: 10px; width:255px;margin: 10px;', 'placeholder' : 'How much Year'}), required = False)
    skills = forms.CharField(max_length=500,
    widget=forms.Textarea(attrs={'class': 'form-field','style': 'margin: 10px;',"rows":5, "cols":20}), required = False)
    location_to_search_job = forms.CharField(max_length=50,
    widget=forms.TextInput(attrs={'class': 'form-field','style': 'height: 10px; width:255px;margin: 10px;', 'placeholder' : 'Type Your Full Name'}), required = False)
    # recommendation = forms.CharField( 
    # widget=forms.BooleanField(required=False))
    class Meta:
        model = Profile
        fields = ('full_name','permanent_address','temporary_address','contact','profession','education','experience_year','skills','location_to_search_job','recommendation')
        # widgets = {
        #     'full_name': forms.TextInput(
        #         attrs={'class': 'form-field','style': 'height: 10px; width:255px; margin: 10px; font-size: 15px','placeholder' : 'Type Your Full Name'}),
        # }
class RegisterEmployerForm(UserAdminCreationForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    company_name = forms.CharField(max_length=50,
    widget=forms.TextInput(attrs={'class': 'form-field','style': 'height: 10px; width:255px;margin: 10px;', 'placeholder' : 'Type Your Company Name'}), required = True)
    company_address = forms.CharField(max_length=50,
    widget=forms.TextInput(attrs={'class': 'form-field','style': 'height: 10px; width:255px;margin: 10px;', 'placeholder' : 'Type Your Company Address'}), required = True)
    company_contact = PhoneNumberField(
         widget=forms.TextInput(attrs={'class': 'form-field','style': 'height: 10px; width:255px;margin: 10px;', 'placeholder' : 'Type Your Company Contact'}), required = True)
    company_bussiness = forms.CharField(max_length=50,
    widget=forms.TextInput(attrs={'class': 'form-field','style': 'height: 10px; width:255px;margin: 10px;', 'placeholder' : 'What is your bussiness?'}), required = True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-field','style': 'height: 10px; width:255px; margin: 10px; font-size: 15px','placeholder' : 'Password'}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class': 'form-field','style': 'height: 10px; width:255px; margin: 10px; font-size: 15px','placeholder' : 'Confirm password'}))
    class Meta:
        model = User
        fields = ('company_name','company_address','company_contact','company_bussiness','email')
        widgets = {
            'email': forms.EmailInput(
                 attrs={'class': 'form-field','style': 'height: 10px; width:255px; margin: 10px; font-size: 15px','placeholder' : 'Type Your Email'}),
            'company_name': forms.TextInput(
                attrs={'class': 'form-field','style': 'height: 10px; width:255px; margin: 10px; font-size: 15px','placeholder' : 'Type Your Company Name'}),
        }
        # user.address_longitude=20.0456
        # fields.address_latitude = 24.367

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterEmployerForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.employer = True
        user.active = False
        if commit:
            user.save()
        return user

class RegisterEmployerChangeForm(forms.ModelForm):

    class Meta:
        model = Register_Company_Detail
        fields = ('company_name','company_address','company_contact','company_bussiness','company_bussiness','address_latitude','address_longitude')



# class SignupForm(forms.ModelForm):

#     full_name = forms.CharField(max_length=50,
#     widget=forms.TextInput(attrs={'class': 'form-field','style': 'width:255px', 'placeholder' : 'Full Name'}))

#     email = forms.EmailField(max_length=254, 
#     widget=forms.TextInput(attrs={'class': 'form-field', 'style': 'width:255px','placeholder' : 'Email'}))
    
#     email_password = forms.CharField(max_length=50,
#     widget=forms.TextInput(attrs={'class': 'form-field', 'style': 'width:255px','placeholder' : 'Password'}))


#     class Meta:
#         model = Register_Detail
#         fields = "__all__"
#     # def clean_email(self):
#     #     email = self.cleaned_data('email')
#     #     if(validate_email(email)):
#     #         try:
#     #             match = Register_Detail.objects.get(email = email)
#     #         except:
#     #             return email
#     #         raise forms.ValidationError("Email already exist")
#     #         return redirect('signup') 
#     #     else:
#     #         raise forms.ValidationError("Email is not valid")
#     #         return redirect('signup') 

#     # def clean_password(self):
#     #     pas = self.cleaned_data['email_password']
#     #     MIN_LENGTH = 8
#     #     if(len(pas) < MIN_LENGTH):
#     #         raise forms.ValidationError("Password must be altleast 8 digits")
#     #     elif(pas.isdigit()):
#     #         raise forms.ValidationError("Password should not be all numeric")
#     #     else:
#     #         return pas

# class SignupFormEmployer(forms.ModelForm):

#     company_email = forms.EmailField(max_length=254, 
#     widget=forms.TextInput(attrs={'class': 'form-field', 'style': 'width:255px','placeholder' : 'Email'}))
    
#     company_password = forms.CharField(max_length=50,
#     widget=forms.TextInput(attrs={'class': 'form-field', 'style': 'width:255px','placeholder' : 'Password'}))

#     company_address = forms.CharField(max_length=50,
#     widget=forms.TextInput(attrs={'class': 'form-field','style': 'width:255px', 'placeholder' : 'eg. kamalpokhari, ktm'}), required = True)

#     company_name = forms.CharField(max_length=50,
#     widget=forms.TextInput(attrs={'class': 'form-field','style': 'width:255px', 'placeholder' : 'eg. Freefox pvt.ltd'}), required = True)

#     company_contact = forms.CharField(max_length=50,
#     widget=forms.TextInput(attrs={'class': 'form-field','style': 'width:255px', 'placeholder' : 'eg. 9843470870'}), required = True)

#     class Meta:
#         model = Register_Detail
#         fields = "__all__"
# class RegisterCompanyForm(forms.ModelForm):
#     company_password = forms.CharField(widget = forms.PasswordInput(
#     attrs={'class': 'form-field','style': 'height: 10px; width:255px; margin: 10px','placeholder' : 'eg. **********'}))

#     class Meta:
#         model = Register_Company_Detail
#         fields = ['company_user','company_name','company_address','company_contact','company_email','company_password']
#         label = {
#             'passowrd': 'company_password'
#         }
#         widgets = {
#             'company_name': forms.TextInput(
#                 attrs={'class': 'form-field','style': 'height: 10px; width:255px; margin: 10px; font-size: 15px','placeholder' : 'eg. Freefox pvt.ltd'}),
#             'company_address': forms.TextInput(
#                  attrs={'class': 'form-field','style': 'height: 10px; width:255px; margin: 10px; font-size: 15px','placeholder' : 'eg. kamalpokhari, ktm'}),
#             'company_contact':forms.TextInput(
#                  attrs={'class': 'form-field','style': 'height: 10px; width:255px; margin: 10px; font-size: 15px','placeholder' : 'eg. 9861504770'}),
#             'company_email':forms.TextInput(
#                  attrs={'class': 'form-field','style': 'height: 10px; width:255px; margin: 10px; font-size: 15px','placeholder' : 'eg. abc123@gmail.com'}),
#         }

#     def clean_email(self):
#         email = self.cleaned_data('company_email')
#         if(validate_email(email)):
#             try:
#                 Register_Company_Detail.objects.get(company_email = email)
#             except:
#                 return email
#             raise ValidationError("Email already exist")
#         else:
#             raise ValidationError("Email is not valid")

#     def save(self):
#         company_password = self.cleaned_data.pop('company_password')
#         u = super().save()
#         u.set_password(company_password)
#         u.save()
#         return u 

class LoginForm(forms.Form):

    email = forms.EmailField(max_length=254, 
    widget=forms.TextInput(attrs={'class': 'form-field','style': 'width:255px', 'placeholder' : 'Email'}))
    
    email_password = forms.CharField(max_length=50,
    widget=forms.PasswordInput(attrs={'class': 'form-field','style': 'width:255px', 'placeholder' : 'Password'}))

    # def clean(self, *args, **kwags):
    #     email = self.cleaned_data.get('email')
    #     email_password = self.cleaned_data.get('email_password')
    #     if email and email_password:
    #         user = authenticate(email=email, email_password=email_password)
    #         if not user:
    #             raise forms.ValidationError('This user doesn not exist')
    #         if not user.check_password(email_password):
    #             raise forms.ValidationError('Incorrect password')
    #         if not user.is_active:
    #             raise forms.ValidationError('This user is not active')
    #         return super(LoginForm, self).clean(*args, **kwargs)

class SearchForm(forms.Form):
    
    available_catagories = [('','All Categories'),('Banking','Banking'),('Engineering','Engineering'),('Information Technology', 'Information Technology'),('Design and Architecture','Design and Architecture'),('Medical Sector','Medical Sector'), ('Marketing and Communications','Marketing and Communications'), ('Education and Training', 'Education and Training'), ('Sports', 'Sports'), ('Legal','Legal'),('Other','Other')]

    catagories = forms.CharField(label='Job Catagory :', 
    widget=forms.Select(choices=available_catagories,attrs={'class': 'form-field','style': 'width:290px'}), required = False)

    # skill = forms.CharField(max_length=50,
    # widget=forms.TextInput(attrs={'class': 'form-field', 'style': 'width:255px','placeholder' : 'Skill'}), required = False)


    place = forms.CharField(max_length=50,
    widget=forms.TextInput(attrs={'class': 'form-field','style': 'width:255px', 'placeholder' : 'Place'}), required = False)

class EndDate(forms.DateInput):
    input_type = 'date'

class VacancyAnnounceForm(forms.ModelForm):

    available_catagories = [('Other','Other'),('Banking','Banking'),('Engineering','Engineering'),('Information_Technology', 'Information Technology'),('Design','Design and Architecture'),('Medical','Medical Sector'), ('Marketer','Marketing and Communications'), ('Education', 'Education and Training'), ('Sports', 'Sports'), ('Legal','Legal')]

    job_category = forms.CharField(label='Job Catagory :', 
    widget=forms.Select(choices=available_catagories,attrs={'class': 'form-field','style': 'width:255px;margin: 10px;'}), required = True)

    job_title = forms.CharField(max_length=50, label='Job Title :', 
    widget=forms.TextInput(attrs={'class': 'form-field', 'style': 'width:225px;margin: 10px;','placeholder' : 'eg. php developer'}), required = True)

    education_categories = [('Below SLC','Below SLC'),('SLC Passed','SLC Passed'),('+2 Passed','+2 Passed'),( 'Bachelor Passed','Bachelor Passed'),('Master Passed', 'Master Passed'), ('PHD Completed', 'PHD completed')]
    
    education = forms.CharField(label='Education Level :', 
    widget=forms.Select(choices=education_categories,attrs={'class': 'form-field','style':'height: 40px; width:255px;margin: 10px;'}), required = False)
   
    experience_year = forms.CharField(label='Expereience Approximate Year :',max_length=50,
    widget=forms.NumberInput(attrs={'class': 'form-field','style': 'height: 10px; width:255px;margin: 10px;', 'placeholder' : 'How much Year'}), required = False)
   
    work_catagories = [('full_time','Full Time'),('part_time','Part Time'),('contract', 'Contract')]

    work_type = forms.CharField(
    widget=forms.Select(choices=work_catagories,attrs={'class': 'form-field','style': 'width:255px;margin: 10px;'}), required = True)

    payment = [('salary', 'Salary'),('hourly', 'Hourly Based'), ('commisssion', 'Commission')]

    payment_type = forms.CharField(
    widget=forms.Select(choices=payment,attrs={'class': 'form-field','style': 'width:255px;margin: 10px;'}), required = True)

    range_of_salary = forms.CharField(max_length=50,
    widget=forms.TextInput(attrs={'class': 'form-field','style': 'width:155px;margin: 10px;', 'placeholder' : 'eg. 10000'}), required = True)

    plus_services = forms.CharField(max_length=50,
    widget=forms.TextInput(attrs={'class': 'form-field','style': 'width:555px;margin: 10px;', 'placeholder' : 'eg. Motorcycle'}), required = False)

    qualification_and_experience = forms.CharField(max_length=500,
    widget=forms.Textarea(attrs={'class': 'form-field','style': 'width:455px;margin: 10px;',"rows":5, "cols":20}), required = True)

    task_and_responsibilities = forms.CharField(max_length=500,
    widget=forms.Textarea(attrs={'class': 'form-field','style': 'width:455px;margin: 10px;',"rows":5, "cols":20}), required = True)

    expiry_date = forms.DateField(
    widget=EndDate(attrs={'class': 'form-field','style': 'width:130px;margin: 10px;'}), required = True)

    class Meta:
        model = Vacancy_Detail
        fields = ('job_category','job_title','work_type','education','experience_year','payment_type','payment_type','range_of_salary','plus_services','task_and_responsibilities','qualification_and_experience','expiry_date')

class CompanyReviewForm(forms.Form):

    choices  = [('Bad','Bad'),('Good','Good'),('Very Good','Very Good')]
    rate = [('Low','Low'),('Medium','Medium'),('High','High')]
    like = [(True,'Yes'), (False,'No')]

    company_name = forms.CharField(max_length=50,
    widget=forms.TextInput(attrs={'class': 'form-field','style': 'width:255px', 'placeholder' : 'eg. Freefox pvt.ltd'}), required = True)
    
    job_title= forms.CharField(max_length=50,
    widget=forms.TextInput(attrs={'class': 'form-field','style': 'width:255px', 'placeholder' : 'eg. Developer'}), required = True)

    working_environment = forms.ChoiceField(required=True,
                            widget=forms.RadioSelect(),
                            choices=choices)

    oppurtunity_rate = forms.ChoiceField(required=True,choices=rate,
    widget=forms.RadioSelect)

    management = forms.ChoiceField(required=True,choices=choices,
    widget=forms.RadioSelect)

    benefits_perks = forms.ChoiceField(required=True,choices=rate,
    widget=forms.RadioSelect)

    facilities = forms.ChoiceField(required=True,choices=choices,
    widget=forms.RadioSelect)

    recommend_other = forms.ChoiceField(required=True,choices=like,
    widget=forms.RadioSelect)

    salary_rate = forms.ChoiceField(required=True,choices=rate,
    widget=forms.RadioSelect) 

    good_things = forms.CharField(max_length=500,
    widget=forms.Textarea(attrs={'class': 'form-field',"rows":5, "cols":20}), required = True)

    challeneges = forms.CharField(max_length=500,
    widget=forms.Textarea(attrs={'class': 'form-field',"rows":5, "cols":20}), required = True)

    company_summary = forms.CharField(max_length=500,
    widget=forms.Textarea(attrs={'class': 'form-field',"rows":5, "cols":20}), required = True)

    class Meta:
        model = Company_Review
        fields = fields = '__all__'