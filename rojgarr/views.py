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
import requests, json, googlemaps
import geopy.geocoders as geocoders 
from geopy.geocoders import Nominatim
from math import *
from django.contrib.auth.hashers import make_password, check_password

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

def header(request):    
        return render(request, 'header.html')

def home(request, cond=None):

    queryset = Vacancy_Detail.objects.select_related('company')
    obj1 = []
    for i in queryset:
        obj1.append({'pk':i.id, 'job_category': i.job_category, 'job_title': i.job_title, 'range_of_salary': i.range_of_salary, 'expiry_date': i.expiry_date, 'company_name': i.company.company_name, 'company_address': i.company.company_address})
    if not obj1:
        messages.success(request, "No any job is available.")  
    form = SearchForm()
    
    # vacancies = Vacancy_Detail.objects.order_by('-date_added')
    paginator = Paginator(obj1, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home.html',{'v_detail': page_obj,'search_form': form, 'cond':cond})

def home_logged_in(request):
    return home(request, cond='yes')

def signup(request):
    form = SignupForm()    
    return render(request, 'signup.html',{'signup_form': form})

def login(request):
    form = LoginForm()
    return render(request,'login.html',{'login_form':form})

def company_review(request):
    return render(request,'company_review.html',{'comapy_review_form': CompanyReviewForm(),'cond':'yes'})

def employer_part(request):
    form = LoginForm()
    return render(request,'log_in_employer.html',{'login_form':form})

def employer_logged_in(request):
    return create_job(request, {'token':'yes'})

def register_employer(request):  
        return render(request, 'sign_up_employer.html',{'signup_form': SignupFormEmployer()})     

def create_job(request, token='None'):
    form = VacancyAnnounceForm()
    return render(request, 'vacancy_announcement.html',{'vacancy_announce_form': form, 'token':token})  

def des (request, pk):
    # v = Vacancy_Detail.objects.get(id=pk)

    # return HttpResponse(v.job_category)
    try:
        v = Vacancy_Detail.objects.select_related('company').get(id = pk)
        return render(request, 'detail_view.html',{'v_detail': v})
    #     obj1 = []
    #     for i in queryset:
    #         if(pk == i.id):
    #             obj1.append({'job_category': i.job_category, 'job_title': i.job_title, 'range_of_salary': i.range_of_salary, 'expiry_date': i.expiry_date, 'company_name': i.company.company_name, 'company_address': i.company.company_address})
    #     if not obj1:
    #         return Response({'error': True, 'Message':'No any vacancies available.'}, status = HTTP_400_BAD_REQUEST)
    #     return Response({'error':False, 'objlist':obj1}, status = HTTP_200_OK)
    except Vacancy_Detail.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)    

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
        if(len(filter2) == 0):
            return render(request, 'home.html',{'length': 0,'search_form': SearchForm()})
        else:
            return render(request, 'home.html',{'v_detail': filter2,'search_form': SearchForm()})

@api_view(['GET','POST'])
def add_vacancy_detail(request, token):
    if request.method == 'POST':
        try:
            form = VacancyAnnounceForm(request.POST)
            values = Vacancy_Detail(
                company = token,
                job_category = request.POST['catagories'],
                job_title =request.POST['job_title'],
                work_type = request.POST['work_type'],
                payment_type = request.POST['payment_type'],
                range_of_salary = request.POST['salary'],
                plus_services = request.POST['plus_services'],
                task_and_responsibilities = request.POST['responsibilities'],
                qualification_and_experience = request.POST['qualifiactions'],
                expiry_date = request.POST['end_date'],
            )
            serializer=VacancySerializer(data=request.data)
            if serializer.is_valid():
                values.save()
                messages.success(request, "Register Successfully !") 
                return redirect('create_job')
            else:
               message.info(request, 'Invalid values detected')
               return render(request, 'vacancy_announcement.html',{'signup_form': form})    

        except:  
            return Response(status=status.HTTP_404_NOT_FOUND)

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

            values = Register_Detail(
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
    
    non = Nominatim()
    li = []
    try:
        n=non.geocode(address)
        li = [n.latitude, n.longitude]
        
    except:
        return None
    return li

# @api_view(['GET','POST'])
# def tri(request):
#     print('a')
#     print(distance_calculation(27.700769,85.300140,27.693298,85.281652))
#     print('b')
#     return None
def distance_calculation(lat1,lon1,lat2,lon2): # calculate the distance between two points according to the geo location
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in 6371 kilometers. Use 3956 for miles
    return c * r

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

def search(request):
    if request.method == 'POST':
        s=request.POST['catagories']
        p=request.POST['place']
        queryset = Vacancy_Detail.objects.select_related('company')
        obj1 = []
        if(s != "" and p == ""):
            for i in queryset:
                if(s == i.job_category):
                    obj1.append({'pk':i.id, 'job_category': i.job_category, 'job_title': i.job_title, 'range_of_salary': i.range_of_salary, 'expiry_date': i.expiry_date, 'company_name': i.company.company_name, 'company_address': i.company.company_address})

        elif(p != "" and s == ""):
            for i in queryset:
                if(p == i.company.company_address):
                    obj1.append({'pk':i.id, 'job_category': i.job_category, 'job_title': i.job_title, 'range_of_salary': i.range_of_salary, 'expiry_date': i.expiry_date, 'company_name': i.company.company_name, 'company_address': i.company.company_address})

        elif(s != "" and p != ""):
            print(s)
            for i in queryset:
                if(s == i.job_category and p == i.company.company_address):
                    obj1.append({'pk':i.id, 'job_category': i.job_category, 'job_title': i.job_title, 'range_of_salary': i.range_of_salary, 'expiry_date': i.expiry_date, 'company_name': i.company.company_name, 'company_address': i.company.company_address})   
        else:
            messages.success(request, "Fill the detail first.")   
        
        if not obj1:
            messages.success(request, "No any job is available.")  

        paginator = Paginator(obj1, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'home.html',{'v_detail': page_obj,'search_form': SearchForm()})


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
#         return Response(status=204)