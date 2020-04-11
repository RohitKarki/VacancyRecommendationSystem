from django import forms
from .models import *
from django.core.validators import validate_email
from django.shortcuts import redirect
from django.core.exceptions import ValidationError 
from django.contrib.auth import authenticate

class SignupForm(forms.ModelForm):

    full_name = forms.CharField(max_length=50,
    widget=forms.TextInput(attrs={'class': 'form-field','style': 'width:255px', 'placeholder' : 'Full Name'}))

    email = forms.EmailField(max_length=254, 
    widget=forms.TextInput(attrs={'class': 'form-field', 'style': 'width:255px','placeholder' : 'Email'}))
    
    email_password = forms.CharField(max_length=50,
    widget=forms.TextInput(attrs={'class': 'form-field', 'style': 'width:255px','placeholder' : 'Password'}))


    class Meta:
        model = Register_Detail
        fields = "__all__"
    # def clean_email(self):
    #     email = self.cleaned_data('email')
    #     if(validate_email(email)):
    #         try:
    #             match = Register_Detail.objects.get(email = email)
    #         except:
    #             return email
    #         raise forms.ValidationError("Email already exist")
    #         return redirect('signup') 
    #     else:
    #         raise forms.ValidationError("Email is not valid")
    #         return redirect('signup') 

    # def clean_password(self):
    #     pas = self.cleaned_data['email_password']
    #     MIN_LENGTH = 8
    #     if(len(pas) < MIN_LENGTH):
    #         raise forms.ValidationError("Password must be altleast 8 digits")
    #     elif(pas.isdigit()):
    #         raise forms.ValidationError("Password should not be all numeric")
    #     else:
    #         return pas

class SignupFormEmployer(forms.ModelForm):

    company_email = forms.EmailField(max_length=254, 
    widget=forms.TextInput(attrs={'class': 'form-field', 'style': 'width:255px','placeholder' : 'Email'}))
    
    company_password = forms.CharField(max_length=50,
    widget=forms.TextInput(attrs={'class': 'form-field', 'style': 'width:255px','placeholder' : 'Password'}))

    company_address = forms.CharField(max_length=50,
    widget=forms.TextInput(attrs={'class': 'form-field','style': 'width:255px', 'placeholder' : 'eg. kamalpokhari, ktm'}), required = True)

    company_name = forms.CharField(max_length=50,
    widget=forms.TextInput(attrs={'class': 'form-field','style': 'width:255px', 'placeholder' : 'eg. Freefox pvt.ltd'}), required = True)

    company_contact = forms.CharField(max_length=50,
    widget=forms.TextInput(attrs={'class': 'form-field','style': 'width:255px', 'placeholder' : 'eg. 9843470870'}), required = True)

    class Meta:
        model = Register_Detail
        fields = "__all__"
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
    widget=forms.TextInput(attrs={'class': 'form-field','style': 'width:255px', 'placeholder' : 'Password'}))

    def clean(self, *args, **kwags):
        email = self.cleaned_data.get('email')
        email_password = self.cleaned_data.get('email_password')
        if email and email_password:
            user = authenticate(email=email, email_password=email_password)
            if not user:
                raise forms.ValidationError('This user doesn not exist')
            if not user.check_password(email_password):
                raise forms.ValidationError('Incorrect password')
            if not user.is_active:
                raise forms.ValidationError('This user is not active')
            return super(LoginForm, self).clean(*args, **kwargs)

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
class VacancyAnnounceForm(forms.Form):

    available_catagories = [('Other','Other'),('Banking','Banking'),('Engineering','Engineering'),('Information_Technology', 'Information Technology'),('Design','Design and Architecture'),('Medical','Medical Sector'), ('Marketer','Marketing and Communications'), ('Education', 'Education and Training'), ('Sports', 'Sports'), ('Legal','Legal')]

    catagories = forms.CharField(label='Job Catagory :', 
    widget=forms.Select(choices=available_catagories,attrs={'class': 'form-field','style': 'width:255px'}), required = True)

    job_title = forms.CharField(max_length=50, label='Job Title :', 
    widget=forms.TextInput(attrs={'class': 'form-field', 'style': 'width:225px','placeholder' : 'eg. php developer'}), required = True)

    work_catagories = [('full_time','Full Time'),('part_time','Part Time'),('contract', 'Contract')]

    work_type = forms.CharField(
    widget=forms.Select(choices=work_catagories,attrs={'class': 'form-field','style': 'width:255px'}), required = True)

    payment = [('salary', 'Salary'),('hourly', 'Hourly Based'), ('commisssion', 'Commission')]

    payment_type = forms.CharField(
    widget=forms.Select(choices=payment,attrs={'class': 'form-field','style': 'width:225px'}), required = True)

    salary = forms.CharField(max_length=50,
    widget=forms.TextInput(attrs={'class': 'form-field','style': 'width:155px', 'placeholder' : 'eg. 10000'}), required = True)

    plus_services = forms.CharField(max_length=50,
    widget=forms.TextInput(attrs={'class': 'form-field', 'placeholder' : 'eg. Motorcycle'}), required = False)

    qualifiactions = forms.CharField(max_length=500,
    widget=forms.Textarea(attrs={'class': 'form-field',"rows":5, "cols":20}), required = True)

    responsibilities = forms.CharField(max_length=500,
    widget=forms.Textarea(attrs={'class': 'form-field',"rows":5, "cols":20}), required = True)

    end_date = forms.DateField(
    widget=EndDate(attrs={'class': 'form-field','style': 'width:130px'}), required = True)
