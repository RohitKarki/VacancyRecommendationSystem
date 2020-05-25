from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework import viewsets
from rest_framework.views import APIView
from .serializers import *
from .forms import *
from rest_framework import status
from django.contrib import messages
import requests, json, googlemaps,schedule, time 
import geopy.geocoders as geocoders 
from geopy.geocoders import Nominatim
from math import *
from django.contrib.auth.hashers import make_password, check_password
from django.views.generic import CreateView, FormView
from .token import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.core.mail import EmailMessage
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User

from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK
)
#from django.urls import reverse_lazy
# Create your views here.
#class vacancies(viewsets.ModelViewSet):
#        queryset = Vacancy_Detail.objects.all()
#        serializer_class = vacancySerializer
from django.core.paginator import Paginator



#  All the above code are the class of packages and modules import 



# class RegisterView(CreateView):
#     form_class = RegisterEmployeForm
#     template_name = 'signup.html'
#     success_url = 'login'



#  this the function for the home page of website for user/visiter

def home(request, cond=None): # cond is the flag for change the menu bar of authenticate and non authenticate person
    try:
        queryset = Vacancy_Detail.objects.select_related('company')
        obj1 = []
        for i in queryset:
            obj1.append({'pk':i.id, 'job_category': i.job_category, 'job_title': i.job_title, 'range_of_salary': i.range_of_salary, 'expiry_date': i.expiry_date, 'company_name': i.company.company_name, 'company_address': i.company.company_address})
        if not obj1:
            messages.success(request, "No any job is available.")  
        form = SearchForm()
        
        # vacancies = Vacancy_Detail.objects.order_by('-date_added')

        # pagination code is invovle here

        paginator = Paginator(obj1, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        #  check the authorization

        if not request.user.is_authenticated:
            return render(request, 'home.html',{'v_detail': page_obj,'search_form': SearchForm(request.POST), 'cond':cond})
        else:

            # check the employe or employer
            if request.user.employe:
                return render(request, 'home.html',{'v_detail': page_obj,'search_form': SearchForm(request.POST), 'cond':'yes'})
            else: # if employer
                return create_job(request) # call the create job function and this times its a front page for authorize user
    
    except Vacancy_Detail.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)  

#  function for home page after log in call the function with cond yes
def home_logged_in(request):
    return home(request, cond='yes')

# function for signup the employee
def signup(request):
    try:
        if request.method == 'POST':
            form = RegisterEmployeForm(request.POST)
            if form.is_valid():
                user = form.save() # save the user in user table
                user.refresh_from_db()  # refresh the database
                user.profile.full_name = form.cleaned_data.get('full_name')    # pass the data using signal function or signal to the profile model     
                user.save() # save the user data according to the form
                
                current_site = get_current_site(request) # this function helps to get the presnt host id 
                subject = 'Activate the Rogarr employe account.' # subject to the gmail after sign up

                #  messages values needed for the message in gmail 
                message = render_to_string('account_activation_email.html', {
                    'user': user,
                    # 'domain': request.META['HTTP_HOST'],
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token': account_activation_token.make_token(user), # generate token to encode in mail for that call to the function 
                }) # render_to_string function call the html page and pass the data into html page

                to_email = form.cleaned_data.get('email') # get the email to gmail
                email = EmailMessage(
                            subject, message, to=[[to_email]]
                ) # call function to email
                email.send()
                # user.email_user(subject, message)
                return redirect('account_activation_sent') # redirect to the account_activation_sent.html page 
                # email = form.cleaned_data.get('email')
                # raw_password = form.cleaned_data.get('password1')
                # user = authenticate(email=email, password=raw_password)
                # login(request, user)
                # return redirect('home')
        else:
            form = RegisterEmployeForm() # set the varaible value as regester empoye form
        return render(request, 'signup.html', {'form': form}) # redirect to sigup page

    except message.DoesNotExist: # exception handling
        return Response(status=status.HTTP_404_NOT_FOUND)  

    # form = SignupForm()    
    # return render(request, 'signup.html',{'signup_form': form})


# function which verify to authenticate the 
def authenticate_user(email, password):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return None
    else:
        if user.check_password(password):
            return user

    return None

# function which help to redirect the log in page and log to the user after log in
def login_employe(request):
    try:
        if request.method == 'POST':
            form = LoginForm(request.POST) # log in form with filed values
            email = request.POST['email'] # get email from form
            password = request.POST['email_password'] # get password from form
            user = authenticate_user(email=email, password=password) # call the autheticate_user function with passing the vlue of email and password
            if user is not None: # condition for user is not None
                if user.employe: # check the user type
                    if user.active: # check the user activate or not
                        login(request, user) # user is log in with default function login
                        return home(request, cond='yes') # call home page with log in condition yes
                    else:
                        # through the message if any message for that it call messages default function 
                        messages.success(request, "Please check your gmail. First you need to confirm from the gmail and then, resubmit it.") 
                        return render(request,'login.html',{'login_form':form})     # redirect to page log in
                else:
                    messages.success(request, "You are not authorized as employe.") 
                    return render(request,'login.html',{'login_form':form}) # redirect to page log in
            else:    
                messages.success(request, "Wrong email or password") 
                return render(request,'login.html',{'login_form':form})
        else:
            return render(request,'login.html',{'login_form':LoginForm()})

    except: # exception handeling
        return Response(status=status.HTTP_404_NOT_FOUND)  

# function to call log in page for employer
def employer_part(request):
    form = LoginForm()
    return render(request,'log_in_employer.html',{'login_form':form})

# function to log in employer
def login_employer(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        email = request.POST['email']
        password = request.POST['email_password']
        user = authenticate_user(email=email, password=password)
        if user is not None:
            if user.employer:
                login(request, user)
                return render(request,'vacancy_announcement.html',{'form':VacancyAnnounceForm(), 'token':'yes'})
            else:
                messages.success(request, "You are not authorized as employer.") 
                return render(request,'log_in_employer.html',{'login_form':form})
        else:    
            messages.success(request, "Wrong email or password") 
            return render(request,'log_in_employer.html',{'login_form':form})
    else:
        return create_job(request)

# functon to register the employer and call the sigup page for employer
def register_employer(request):  
    try:
        if request.method == 'POST':
            form = RegisterEmployerForm(request.POST)  # set the variable with form and posted values
            li=[]
            li = location_lat_lon(request.POST['company_address']) #call the function for address longitude and latitude
            if li is None:
                # message the below mesage if location longitude and latitude is found by the function
                messages.success(request, "Location is not valid.Please enter the valid address without mistake the spelling.")  
                return render(request, 'sign_up_employer.html',{'form': form})  # call the register form
    
            if form.is_valid(): #check form validation
                user = form.save() # save the user through user model
                #  set the values for save the values in register_company_detail model
                values = Register_Company_Detail(
                    company_address = request.POST['company_address'],
                    company_name = request.POST['company_name'],
                    company_contact = request.POST['company_contact'],
                    company_bussiness = request.POST['company_bussiness'],
                    address_latitude = li[0],
                    address_longitude = li[1],
                    user = user
                )  
                values.save() #save the values
                current_site = get_current_site(request) # get the current site id to pass in email
                subject = 'Activate the Rogarr employer account.' # subject for email
                # message to send in email and passes to the activation_email.html page
                message = render_to_string('account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token': account_activation_token.make_token(user), # code encode to send in mail
                })
                to_email = form.cleaned_data.get('email') # get the to whom the email sent
                email = EmailMessage(
                            subject, message, to=[[to_email]]
                )
                email.send() # dend email
                # user.email_user(subject, message)
                return redirect('account_activation_sent') # redirect the activation_email_page
                # email = form.cleaned_data.get('email')
                # raw_password = form.cleaned_data.get('password1')
                # user = authenticate(email=email, password=raw_password)
                # login(request, user)
                # return redirect('employer')
        # condition to call the register page
        else:
            form = RegisterEmployerForm()
        return render(request, 'sign_up_employer.html', {'form': form})    
            # return render(request, 'sign_up_employer.html',{'signup_form': SignupFormEmployer()})     
    except Register_Company_Detail.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)  

# function to call the account activation_sent page
def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')  

# function to verify the email return back link with decoding the token
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64)) # decode the token
        user = User.objects.get(pk=uid) # get the values through id

    except (TypeError, ValueError, OverflowError, User.DoesNotExist): # exception handling
        user = None

    if user is not None and account_activation_token.check_token(user, token): # condition the permission after token verify user
        user.active = True # user is activated after click the link
        user.save() # savte the activation on datbase
        # login(request, user)
        return redirect('home') # redirect to the home page
    else: # after code is wrong 
        return render(request, 'account_activation_invalid.html') 

#  function to direct the form for vacancy announcement
def create_job(request):
    try:
        form = VacancyAnnounceForm()
        return render(request, 'vacancy_announcement.html',{'vacancy_announce_form': form, 'token':'yes'})  
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)  

#  function log ou the employer
def logout_employer(request):
    logout(request) # bulit in function to log out
    return redirect('employer')

# function to log out emoloye
def logout_employe(request):
    logout(request)
    return redirect('home') 

# function to redirect the user profile:
def user_profile(request):
    try:
        if request.user.employe:
            return render(request, 'normal_user_profile.html',{'cond':'yes'})
        elif request.user.employer:
            pass
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)  

# function to edit the profile of employee
def edit_profile(request):
    try:
        if request.method == 'POST':
            form = EditProfileForm(request.POST) # call the edit profile form
            if form.is_valid(): # check the form validation
                if request.POST.get('recommendation', False) is not False: # check the user is ready to recommendation to him/her
                    if request.POST['profession'] == 'None': # it is compulsary for recommendation. so it check it
                        messages.success(request, "Profession must not be None.")  
                        return render(request, 'edit_profile.html',{'form': form, 'cond': 'yes'})  
                    if request.POST['education'] == 'None': # it is compulsary to recommendation. so it check it
                        messages.success(request, "Education must not be None.")  
                        return render(request, 'edit_profile.html',{'form': form, 'cond': 'yes'})  
                    li=[]
                    li = location_lat_lon(request.POST['location_to_search_job']) #call the function for address longitude and latitude
                    if li is None: # check the conditiion the location long and lat is determine by function or not
                        messages.success(request, "Search Location is not valid.Please enter the valid address without mistake the spelling.")  
                        return render(request, 'edit_profile.html',{'form': form, 'cond': 'yes'})  
                    else:
                        request.user.profile.address_latitude = li[0] # save the value through signal in profile model
                        request.user.profile.address_longitude = li[1] # save the value through signal in profile model
                        request.user.profile.recommendation = True # save the value through signal in profile model
                else: # if recommendation is not needed
                    request.user.profile.recommendation = False

                # save the value through signal in profile model
                request.user.profile.full_name = request.POST['full_name']
                request.user.profile.permanent_address = request.POST['permanent_address']
                request.user.profile.temporary_address = request.POST['temporary_address']
                request.user.profile.contact = request.POST['contact']
                request.user.profile.profession = request.POST['profession']
                request.user.profile.education = request.POST['education']
                request.user.profile.experience_year = request.POST['experience_year']
                request.user.profile.skills = request.POST['skills']
                request.user.profile.location_to_search_job = request.POST['location_to_search_job']
            
                request.user.save() # save all the guiven values
                return render(request, "normal_user_profile.html", {'cond': 'yes'})
        else:
            # pass the alreadt save value into the from and call the edit profile page
            obj = Profile.objects.get(id=request.user.profile.id)
            form = EditProfileForm(request.POST or None, instance=obj) # value are instance to the form
            context = {
                'form': form,
                'cond': 'yes'
            }
            return render(request, "edit_profile.html", context)

    except :
        return Response(status=status.HTTP_404_NOT_FOUND)  

#  function which help to show the detail view/page of vacancy detail
def des (request, pk):
    # v = Vacancy_Detail.objects.get(id=pk)

    # return HttpResponse(v.job_category)
    try:
        v = Vacancy_Detail.objects.select_related('company').get(id = pk)
        if not request.user.is_authenticated:
            return render(request, 'detail_view.html',{'v_detail': v})
        return render(request, 'detail_view.html',{'v_detail': v, 'cond':'yes'})
    #     obj1 = []
    #     for i in queryset:
    #         if(pk == i.id):
    #             obj1.append({'job_category': i.job_category, 'job_title': i.job_title, 'range_of_salary': i.range_of_salary, 'expiry_date': i.expiry_date, 'company_name': i.company.company_name, 'company_address': i.company.company_address})
    #     if not obj1:
    #         return Response({'error': True, 'Message':'No any vacancies available.'}, status = HTTP_400_BAD_REQUEST)
    #     return Response({'error':False, 'objlist':obj1}, status = HTTP_200_OK)
    except Vacancy_Detail.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)    

# function to the vacancy detail 
@api_view(['GET','POST'])
def add_vacancy_detail(request):
    if request.method == 'POST':
        try:
            form = VacancyAnnounceForm(request.POST) # call the vacancy form function with por values
            values = Vacancy_Detail(
                company = request.user.register_company_detail,
                job_category = request.POST['job_category'],
                job_title =request.POST['job_title'],
                education = request.POST['education'],
                experience_year = request.POST['experience_year'],
                work_type = request.POST['work_type'],
                payment_type = request.POST['payment_type'],
                range_of_salary = request.POST['range_of_salary'],
                plus_services = request.POST['plus_services'],
                task_and_responsibilities = request.POST['task_and_responsibilities'],
                qualification_and_experience = request.POST['qualification_and_experience'],
                expiry_date = request.POST['expiry_date'],
            ) # set the values according to the model
            if form.is_valid(): # check the form is valid or not
                values.save() # save the values
                messages.success(request, "Register Successfully !") 
                return redirect('announce_vacancy') # redirect to announce vacancy page
            else:
               messages.info(request, 'Invalid values detected')
               return render(request, 'vacancy_announcement.html',{'form': form, 'token':'yes'})    

        except:  
            return Response(status=status.HTTP_404_NOT_FOUND)
    else: 
        form = VacancyAnnounceForm()
        return render(request, 'vacancy_announcement.html',{'form': form, 'token':'yes'}) 

#  function to obtain longitute and latitde address
def location_lat_lon(address):
    # api =  "https://maps.googleapis.com/maps/api/place/nearbysearch/json
#   ?location=-33.8670522,151.1957362
#   &radius=500
#   &types=food
#   &name=harbour
#   &key=AIzaSyAgAjrZxjYUw0LWntNYH8r3V189KZNSJV8
    # print('ok')
    # gmaps_key = googlemaps.Client(key="AIzaSyCICPPHTwVsFYPCHvhDbiD9S5-N-BtxP28")
    # print(gmaps_key)
    # geocode_result = gmaps_key.geocode(address)
    # print('yes')
    # try:
    #     lat = geocode_result[0]["geometry"]["location"]["lat"]
    #     lon = geocode_result[0]["geometry"]["location"]["lon"]

    # except:
    #     lat = None
    #     lon = None

    # print(lat)
    # print(lon)
    # return (lat)
    
    non = Nominatim() # set the nomiation function in varaible
    li = []
    try:
        n=non.geocode(address) # by the help of nomination nad geocode get address log and lat determine
        li = [n.latitude, n.longitude] # add the address long and lat in list
        
    except:
        return None # return non if not found
    return li

def distance_calculation(lat1,lon1,lat2,lon2): # calculate the distance between two points according to the geo location
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in 6371 kilometers. Use 3956 for miles
    return c * r # return the distance them

# function to filter the vacacnicea according to the searched value
def search(request):
    if request.method == 'POST':
        s=request.POST['catagories']
        p=request.POST['place']
        queryset = Vacancy_Detail.objects.select_related('company') # using select qury to get vacancies according to the company
        obj1 = []
        if(s != "" and p == ""): # condition if it is search on the basic of place only
            for i in queryset:
                if(s == i.job_category):
                    obj1.append({'pk':i.id, 'job_category': i.job_category, 'job_title': i.job_title, 'range_of_salary': i.range_of_salary, 'expiry_date': i.expiry_date, 'company_name': i.company.company_name, 'company_address': i.company.company_address})

        elif(p != "" and s == ""):  # condition if it is search on the basic of categories only
            for i in queryset:
                if(p == i.company.company_address):
                    obj1.append({'pk':i.id, 'job_category': i.job_category, 'job_title': i.job_title, 'range_of_salary': i.range_of_salary, 'expiry_date': i.expiry_date, 'company_name': i.company.company_name, 'company_address': i.company.company_address})

        elif(s != "" and p != ""): # if categories and plces values are empty
            for i in queryset:
                if(s == i.job_category and p == i.company.company_address):
                    obj1.append({'pk':i.id, 'job_category': i.job_category, 'job_title': i.job_title, 'range_of_salary': i.range_of_salary, 'expiry_date': i.expiry_date, 'company_name': i.company.company_name, 'company_address': i.company.company_address})   
        else:
            messages.success(request, "Fill the detail first.")   
        
        if not obj1:
            messages.success(request, "No any job is available.")  

        # pagination after data filter 
        paginator = Paginator(obj1, 100) # data hold in page one
        page_number = request.GET.get('page') 
        page_obj = paginator.get_page(page_number) # implement the page number through paginaing function
        # return render(request, 'home.html',{'v_detail': page_obj,'search_form': SearchForm()})
        if not request.user.is_authenticated: # check the authenticated user is searching or not
            return render(request, 'home.html',{'v_detail': page_obj,'search_form': SearchForm(request.POST), 'cond':None})
        else:
            if request.user.employe: 
                return render(request, 'home.html',{'v_detail': page_obj,'search_form': SearchForm(request.POST), 'cond':'yes'})
            else:
                return create_job(request)

# function to apply from the user profile
def confirmation_to_apply(request, pk):
    
    if not request.user.is_authenticated or not request.user.employe:
        return render(request, 'login.html',{'login_form':LoginForm()})
    else:
        lis=[]
        vacancy_detail = Vacancy_Detail.objects.get(id = pk) # pk is the id of selected vacancy detail
        to_email = vacancy_detail.company.user.email # to the email id to mail

        # varaible set need in mail
        full_name = request.user.profile.full_name
        temporary_address = request.user.profile.temporary_address
        permanent_address = request.user.profile.permanent_address
        education = request.user.profile.education
        profession = request.user.profile.profession
        skills = request.user.profile.skills
        experience = request.user.profile.experience_year
        contact = request.user.profile.contact
        email = request.user.email

        #  add the varaible in list
        lis.append(full_name)
        lis.append(temporary_address)
        lis.append(permanent_address)
        lis.append(education)
        lis.append(profession)
        lis.append(skills)
        lis.append(experience)
        lis.append(contact)
        lis.append(email)
        lis.append(vacancy_detail.job_title)

        #  call the email to apply function for mail with providing the list of needed varaible
        email_to_apply_job(to_email = to_email, lis = lis)
        messages.success(request, "Your apply is succesfully done.") 
        return render(request, 'detail_view.html',{ 'v_detail' : vacancy_detail, 'cond':'yes'})

# function to mail when apply by employee
def email_to_apply_job(to_email, lis ):
    subject = 'Rojgarr inform you the profile is intrested on your job.'
    message = render_to_string('email_for_apply.html', {
        'full_name': lis[0],
        'temporary_address': lis[1],
        'permanent_address': lis[2],
        'education': lis[3],
        'profession': lis[4],
        'skills': lis[5],
        'experience': lis[6],
        'contact': lis[7],
        'email': lis[8],
        'job_title': lis[9],
        })
    to_email = to_email
    email = EmailMessage(
                subject, message, to=[[to_email]]
    )
    email.send()



# function to the page for all the company review are shown
def all_company_reviews(request):
    try:
        queryset = Company_Review.objects.select_related('email') # select all the companies
        obj1 = [] 
        for i in queryset: # loops for all the rewier are added in list
            obj1.append({'pk':i.id, 'company_name': i.company_name, 'job_title': i.job_title}) # append the data
        if not obj1:
            messages.success(request, "No any job is available.")  # message if object is not available
    
        # pagination code is invovle here

        paginator = Paginator(obj1, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        #  check the authorization

        if not request.user.is_authenticated:
            return render(request, 'all_company_reviews.html',{'v_detail': page_obj, 'cond': None})
        else:

            # check the employe or employe
            if request.user.employe:
                return render(request, 'all_company_reviews.html',{'v_detail': page_obj, 'cond':'yes'})
    
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)  

# function for the detail view of company_review
def description_comapny_review (request, pk):
    try:
        v = Company_Review.objects.select_related('email').get(id = pk)
        if not request.user.is_authenticated:
            return render(request, 'detail_company_review.html',{'v_detail': v})
        return render(request, 'detail_company_review.html',{'v_detail': v, 'cond':'yes'})
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)   

#  function to check user is authenticate or not to give his/her company review
def company_review(request):
    try: 
        if not request.user.is_authenticated:
            return render(request, 'login.html',{'login_form':LoginForm()})
        else:
            return render(request,'company_review.html',{'comapy_review_form': CompanyReviewForm(), 'cond':'yes'}) 
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)  

# function to save the company review given by the user
def company_review_by_user(request):  
    try:
        if request.method == 'POST':
            form = CompanyReviewForm(request.POST) # from of comapny review with data
            if form.is_valid(): #check form validation
                values = Company_Review( 
                    email = request.user.profile,
                    company_name = request.POST['company_name'],
                    job_title = request.POST['job_title'],
                    oppurtunity_rate = request.POST['oppurtunity_rate'],
                    working_environment = request.POST['working_environment'],
                    management = request.POST['management'],
                    benefits_perks = request.POST['benefits_perks'],
                    facilities = request.POST['facilities'],
                    recommend_other = request.POST['recommend_other'],
                    salary_rate = request.POST['salary_rate'],
                    good_things = request.POST['good_things'],
                    challeneges = request.POST['challeneges'],
                    company_summary = request.POST['company_summary'],
                )  # set the form values in variable s to save
                values.save() #save the values
    
        else:
            form = CompanyReviewForm()
        return redirect('home')
    except Company_Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)  





# ALl the below codes are the acivities which are done for try to make this app.
# So, I doesn't comment it.

class Vacancies(APIView):
    def get(self, request):
        obj = Vacancy_Detail.objects.all()
        serializer = VacancySerializer(obj , many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VacancySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD__REQUEST)

class User_detail(APIView):
    def get(self, request):
        obj = Register_Detail.objects.all()
        serializer = RegisterSerializer(obj , many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD__REQUEST)       

class Register_user(APIView):
    def signup(self, request):
        form = SignupForm()    
        return render(request, 'signup.html',{'signup_form': form}) 

@api_view(['GET','POST'])
def Search_Value(request):
    # print(s)
    # return render(request, 'login.html',{'login_form': LoginForm()})
    if(request.method == 'POST'):
        s = request.POST['catagories']
        p = request.POST['place']  

        print('a')
        if(s != "" and p == ""):
            url = "http://127.0.0.1:8000/Catagory/"+ s + "/Search_Vacancies"

        elif(p != "" and s == ""):
            url = "http://127.0.0.1:8000/Location/"+ p

        elif(s != "" and p != ""):
            url = "http://127.0.0.1:8000/Search_Vacancies/Catagory/Location/" + s + "/" + p
            
        else:
            print('b')
            return Response(status=status.HTTP_404_NOT_FOUND)
        print(url)
        r = requests.get(url)
        # return Response({'error':False, 'v_detail':r}, status = HTTP_200_OK)
        # obj1 = []
        # for i in r:
        #     if(s == i.job_category):
        #         obj1.append({'job_category': i.job_category, 'job_title': i.job_title, 'range_of_salary': i.range_of_salary, 'expiry_date': i.expiry_date, 'company_name': i.company.company_name, 'company_address': i.company.company_address})
        if not r:
            return Response({'error': True, 'Message':'No any vacancies available.'}, status = HTTP_400_BAD_REQUEST)          
        return Response({'error':False, 'v_detail':r}, status = HTTP_200_OK)
        json_response = r.json()
        filter1=[]
        filter1 = json_response  

        return render(request, 'home.html',{'v_detail': filter1,'search_form': SearchForm()})


class Call_Search(APIView):
    def get(self, request):
        print('a')
        return redirect('signup')
        if request.method == 'POST':
            print('a')
            return redirect('signup')
            # s = request.POST['catagories']
            # p = request.POST['place']
            # a = 'http://127.0.0.1:8000/Search/'.join(s)
            # print (p)
            # b = "http://127.0.0.1:8000/Catagory/"+ p + "/Search_Vacancies"
                    
            # r = requests.get(b)
            # print(r)

            # return render(request, 'home.html',{'v_detail': r,'search_form': SearchForm()})
            # return render(request, "http://127.0.0.1:8000/".format(skill=s, place=p))


class Search(APIView):
    def get(self, request, skill, place):
        url = 'http://127.0.0.1:8000/Vacancies/'
        r = requests.get(url)
        json_response = r.json()
        filter1=[]
        filter2=[]
        if(skill == "" and place == ""):
            messages.success(request, "First fill the field. Please ")
            return redirect('home')
        else:
            if(skill == ""):
                filter1 = json_response
            else:
                for j in json_response:
                    if(j['skill'] == skill):
                        contain={
                            'company_name' : j['company_name'],
                            'company_address' : j['company_address'],
                            'skill' : j['skill'],
                            'salary' : j['salary'],
                            'urgent' : j['urgent']
                        }
                        filter1.append(contain) 


            if(place == ""):
                filter2 = filter1
            else:
                for j in filter1:
                    if(j['company_address'] == place):
                        contain={
                            'company_name' : j['company_name'],
                            'company_address' : j['company_address'],
                            'skill' : j['skill'],
                            'salary' : j['salary'],
                            'urgent' : j['urgent']
                        } 
                        filter2.append(contain)     
        print('abc')
        paginator = Paginator(filter2, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        if(len(filter2) == 0):
            return render(request, 'home.html',{'length': 0,'search_form': SearchForm()})
        else:
            return render(request, 'home.html',{'v_detail': page_obj,'search_form': SearchForm()})




@api_view(['GET','POST'])
def user_detail(request):

    # if request.method == 'GET':
        # obj = Register_Detail.objects.all()
        # serializer = RegisterSerializer(obj , many = True)
        # return Response(serializer.data)
    

    if request.method == 'POST':
        try:
            # hasssing the password
            password = make_password(request.POST['email_password'])

            values = User(
                full_name = request.POST['full_name'],
                email = request.POST['email'],
                email_password = password
            )
            form = SignupForm(request.POST)        
            serializer=RegisterSerializer(data=request.data)
            if serializer.is_valid():
                email = request.POST['email']
                if(Register_Detail.objects.get(email = email)):
                        messages.success(request, email + ' already exist!')    
                        return render(request, 'signup.html',{'signup_form': form}) 
                else:
                    values.save()
                    messages.success(request, "Register Successfully !")    
                return redirect('signup') 
            else:
                messages.success(request, "Email is not valid !")  
                return render(request, 'signup.html',{'signup_form': form})  
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    # elif request.method == 'POST':

    #     form = SignupForm(request.POST);          
    #     serializer = RegisterSerializer(data=request.data)
    #     if serializer.is_valid():
    #         url ='http://127.0.0.1:8000/userdetail/'
    #         r = requests.get(url)
    #         json_response = r.json()

    #         for j in json_response:
    #             if(j['email'] == request.POST['email']):
    #                 messages.success(request, j['email'] + ' already exist!')    
    #                 return redirect('signup')

    #         serializer.save()
    #         messages.success(request, "Register Successfully !")    
    #         return redirect('signup') 
    #     else:
    #         messages.success(request, "Email is not valid !")  
    #         return render(request, 'signup.html',{'signup_form': form})   


@api_view(['POST'])
def employer_user_detail(request):

    # if request.method == 'GET':
    #     obj = Register_Company_Detail.objects.all()
    #     serializer = RegisterCompanySerializer(obj , many = True)
    #     return Response(serializer.data)

    if request.method == 'POST':
        try:
            form = SignupFormEmployer(request.POST)   
            address = request.POST['company_address']
            li=[]
            li = location_lat_lon(address) #call the function for address longitude and latitude
            if li is None:
                messages.success(request, "Location is not valid.Please enter the valid address.")  
                return render(request, 'sign_up_employer.html',{'signup_form': form})  
            else:  
                serializer = RegisterCompanySerializer(data=request.data)
                # hasssing the password
                password = make_password(request.POST['company_password'])
                values = Register_Company_Detail(
                    company_name = request.POST['company_name'],
                    company_address = request.POST['company_address'],
                    company_contact = request.POST['company_contact'],
                    company_email = request.POST['company_email'],
                    company_password = password,
                    address_latitude = li[0],
                    address_longitude = li[1]
                )
                if serializer.is_valid():
                    email = request.POST['company_email']
                    print('a')
                    if(Register_Company_Detail.objects.filter(company_email = email)):
                        print('b')
                        messages.success(request, email + ' already exist!')    
                        return redirect('employer_sign_up')
                    else:                
                        values.save()
                        messages.success(request, "Register Successfully !")    
                        return redirect('employer_sign_up') 
                else:
                    messages.success(request, "Email is not valid !")  
                    return render(request, 'sign_up_employer.html',{'signup_form': form})  
            
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # print('0')
        # # location_lat_lon(request.POST['company_address'])
        # form = SignupFormEmployer(request.POST)     
        # serializer = RegisterCompanySerializer(data=request.data)
        # values = Register_Company_Detail(
        #     company_name = request.POST['company_name'],
        #     company_address = request.POST['company_address'],
        #     company_contact = request.POST['company_contact'],
        #     company_email = request.POST['company_email'],
        #     company_password = request.POST['company_password']
        # )
        # if serializer.is_valid():
        #     url ='http://127.0.0.1:8000/employer/userdetail/'
        #     r = requests.get(url)
        #     json_response = r.json()

        #     for j in json_response:
        #         if(j['company_email'] == request.POST['company_email']):
        #             messages.success(request, j['company_email'] + ' already exist!')    
        #             return redirect('employer_sign_up')
                    
        #     values.save()
        #     messages.success(request, "Register Successfully !")    
        #     return redirect('employer_sign_up') 
        # else:
        #     messages.success(request, "Email is not valid !")  
        #     return render(request, 'sign_up_employer.html',{'signup_form': form})  


# @api_view(['GET','POST'])
# def tri(request):
#     print('a')
#     print(distance_calculation(27.700769,85.300140,27.693298,85.281652))
#     print('b')
#     return None


class Search_From_Skill_Location(APIView):
    def get(self,request,s,l):  
        if request.method == 'GET':
            try:
                queryset = Vacancy_Detail.objects.select_related('company')
                obj1 = []
                for i in queryset:
                    if(s == i.job_category and l == i.company.company_address):
                        obj1.append({'job_category': i.job_category, 'job_title': i.job_title, 'range_of_salary': i.range_of_salary, 'expiry_date': i.expiry_date, 'company_name': i.company.company_name, 'company_address': i.company.company_address})
                if not obj1:
                    return Response({'error': True, 'Message':'No any vacancies available.'}, status = HTTP_400_BAD_REQUEST)
                return Response({'error':False, 'objlist':obj1}, status = HTTP_200_OK)
            except Vacancy_Detail.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            # serializer = VacancySerializer(obj1, many=True)
            # return Response(serializer.data)  

class Search_From_Skill(APIView):
    def get(self,request,s):
        if request.method == 'GET':
            try:
                queryset = Vacancy_Detail.objects.select_related('company')
                obj1 = []
                for i in queryset:
                    if(s == i.job_category):
                        obj1.append({'job_category': i.job_category, 'job_title': i.job_title, 'range_of_salary': i.range_of_salary, 'expiry_date': i.expiry_date, 'company_name': i.company.company_name, 'company_address': i.company.company_address})
                if not obj1:
                    return Response({'error': True, 'Message':'No any vacancies available.'}, status = HTTP_400_BAD_REQUEST)
                return Response({'error':False, 'objlist':obj1}, status = HTTP_200_OK)
            except Vacancy_Detail.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND) 

class Search_From_Location(APIView):
    def get(self,request,l):
        if request.method == 'GET':
            try:
                queryset = Vacancy_Detail.objects.select_related('company')
                obj1 = []
                for i in queryset:
                    if(l == i.company.company_address):
                        obj1.append({'job_category': i.job_category, 'job_title': i.job_title, 'range_of_salary': i.range_of_salary, 'expiry_date': i.expiry_date, 'company_name': i.company.company_name, 'company_address': i.company.company_address})
                if not obj1:
                    return Response({'error': True, 'Message':'No any vacancies available.'}, status = HTTP_400_BAD_REQUEST)
                return Response({'error':False, 'objlist':obj1}, status = HTTP_200_OK)
            except Vacancy_Detail.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def specific_vacancy_detail(request,s,l):
    

    if request.method == 'GET':
        if(s != "" and l != ""):
            try:
                obj = Vacancy_Detail.objects.filter(skill = s)
                obj1 = obj.filter(company_address = l)
            except Vacancy_Detail.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
        else:
            if(s != "" and l == ""):
                obj1 = Vacancy_Detail.objects.filter(skill = s)
                
            if(l !="" and s == ""):
                obj1 = Vacancy_Detail.objects.filter(company_address = l)
        serializer = VacancySerializer(obj1, many=True)
        return Response(serializer.data)  

def verified_login(request):
    form = LoginForm(request.POST)
    # url ='http://127.0.0.1:8000/userdetail/'
    # r = requests.get(url)
    # json_response = r.json()

    # for j in json_response:
    #     if(j['email'] == request.POST['email']):    
    #         if(j['email_password'] == request.POST['email_password']):
    #             return redirect('home')
    #         messages.success(request, "Incorrect password !")    
    #         return render(request, 'login.html',{'login_form': form})    
    # messages.success(request, "Email not found !")
    # return render(request,'login.html',{'login_form':form})

    if request.method == 'POST': 
        email = request.POST['email']
        try:
            obj = Register_Detail.objects.get(email = email)
        except Register_Detail.DoesNotExist:
            messages.info(request, 'Email does not exist.')
            return render(request,'login.html',{'login_form':form})
        confirmation_password = check_password(request.POST['email_password'],obj.email_password)
        print(confirmation_password)
        if(confirmation_password):            
            return home(request, cond='yes')
        else:
            messages.info(request, 'Invalid password')
            return render(request,'login.html',{'login_form':form})

def employer_verified_login(request):
    form = LoginForm(request.POST)

    if request.method == 'POST': 
        email = request.POST['email']
        try:
            obj = Register_Company_Detail.objects.get(company_email = email)
        except Register_Company_Detail.DoesNotExist:
            messages.info(request, 'Email does not exist.')
            return render(request,'log_in_employer.html',{'login_form':form})
        confirmation_password = check_password(request.POST['email_password'],obj.company_password)
        print(confirmation_password)
        if(confirmation_password):            
            return employer_logged_in(request)
        else:
            messages.info(request, 'Invalid password')
            return render(request,'log_in_employer.html',{'login_form':form})

# def registration(request):
    
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             new_registration = Register_Detail(email=request.POST['email'], email_password=request.POST['email_password'])
#             new_registration.save()
#             return redirect('home')  
#     else:
#         form = SignupForm()    
#     #context = {'signupForm' : form}
#     return render(request, 'signup.html',{'signup_form': form})



# from django.contrib.auth import login as django_login, logout as django_logout
# from rest_framework.authtoken.models import Token
# from rest_framework.authentication import TokenAuthentication


# class LoginView(APIView):
#     def post(self, request):
#         serializer = LoginSerilizer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data["user"]
#         django_login(request, user)
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({"token": token.key}, status=200)

# class LogoutView(APIView):
#     authentication_clasess = {TokenAuthentication}

#     def post(self, request):
#         django_logout(request)

