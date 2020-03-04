from django import forms
from .models import *
from django.core.validators import validate_email
from django.shortcuts import redirect

class SignupForm(forms.Form):

    full_name = forms.CharField(max_length=50,
    widget=forms.TextInput(attrs={'class': 'form-field', 'placeholder' : 'Full Name'}))

    email = forms.EmailField(max_length=254, 
    widget=forms.TextInput(attrs={'class': 'form-field', 'placeholder' : 'Email'}))
    
    email_password = forms.CharField(max_length=50,
    widget=forms.TextInput(attrs={'class': 'form-field', 'placeholder' : 'Password'}))

    class Meta:
        model = Register_Detail
        fields = ('email')

    def clean_email(self):
        email = self.cleaned_data('email')
        if(validate_email(email)):
            try:
                match = Register_Detail.objects.get(email = email)
            except:
                return email
            raise forms.ValidationError("Email already exist")
            return redirect('signup') 
        else:
            raise forms.ValidationError("Email is not valid")
            return redirect('signup') 

    # def clean_password(self):
    #     pas = self.cleaned_data['email_password']
    #     MIN_LENGTH = 8
    #     if(len(pas) < MIN_LENGTH):
    #         raise forms.ValidationError("Password must be altleast 8 digits")
    #     elif(pas.isdigit()):
    #         raise forms.ValidationError("Password should not be all numeric")
    #     else:
    #         return pas

class LoginForm(forms.Form):

    email = forms.EmailField(max_length=254, 
    widget=forms.TextInput(attrs={'class': 'form-field', 'placeholder' : 'Email'}))
    
    email_password = forms.CharField(max_length=50,
    widget=forms.TextInput(attrs={'class': 'form-field', 'placeholder' : 'Password'}))


class SearchForm(forms.Form):

    skill = forms.CharField(max_length=50,
    widget=forms.TextInput(attrs={'class': 'form-field', 'placeholder' : 'Skill'}), required = False)

    place = forms.CharField(max_length=50,
    widget=forms.TextInput(attrs={'class': 'form-field', 'placeholder' : 'Place'}), required = False)
