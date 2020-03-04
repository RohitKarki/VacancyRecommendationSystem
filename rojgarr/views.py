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
import requests
#from django.urls import reverse_lazy
# Create your views here.
#class vacancies(viewsets.ModelViewSet):
#        queryset = Vacancy_Detail.objects.all()
#        serializer_class = vacancySerializer

def header(request):    
        return render(request, 'header.html')

def home(request):
    form = SearchForm()
    vacancies = Vacancy_Detail.objects.order_by('-date_added')
    return render(request, 'home.html',{'v_detail': vacancies,'search_form': form})

def signup(request):
    form = SignupForm()    
    return render(request, 'signup.html',{'signup_form': form})

def login(request):
    form = LoginForm()
    return render(request,'login.html',{'login_form':form})

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

class UserDetail(APIView):
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

class RegisterUser():
    def signup():
        if request.method == 'POST':
            pass

class Search(APIView):
    def get(self, request, place, skill):
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
def user_detail(request):

    if request.method == 'GET':
        obj = Register_Detail.objects.all()
        serializer = RegisterSerializer(obj , many = True)
        return Response(serializer.data)

    elif request.method == 'POST':
        form = SignupForm();

        if form.is_valid():
            print('yes')
        else:
            print('no')      

        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            url ='http://127.0.0.1:8000/userdetail/'
            r = requests.get(url)
            json_response = r.json()

            for j in json_response:
                if(j['email'] == request.POST['email']):
                    messages.success(request, j['email'] + ' already exist!')    
                    return redirect('signup')
                else:  
                    serializer.save()
                    messages.success(request, "Register Successfully !")    
                    return redirect('signup') 
        else:
            messages.success(request, "Email is not valid !")    
            return redirect('signup') 

@api_view(['GET'])
def specific_vacancy_detail(request,pk):
    try:
        obj = Vacancy_Detail.objects.get(id = pk)
    except Vacancy_Detail.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = VacancySerializer(obj)
    return Response(serializer.data)  

def verified_login(request):
    form = LoginForm()
    url ='http://127.0.0.1:8000/userdetail/'
    r = requests.get(url)
    json_response = r.json()

    for j in json_response:
        if(j['email'] == request.POST['email']):    
            if(j['email_password'] == request.POST['email_password']):
                return redirect('home')
            messages.success(request, "Incorrect password !")    
            return redirect('login')    
    messages.success(request, "Email not found !")
    return render(request,'login.html',{'login_form':form})

    # if request.method == 'POST':
    #     try:
    #         obj = Register_Detail.objects.get(email = request.POST['email']) or Vacancy_Detail.objects.get(email_password = request.POST['email_password'])
    #     except Register_Detail.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #     serializer = registerSerializer(obj)
    #     return Response(serializer.data)


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
    url = 'http://127.0.0.1:8000/Vacancies/'
    r = requests.get(url)
    json_response = r.json()
    filter1=[]
    filter2=[]
    if(request.POST['skill'] == "" and request.POST['place'] == ""):
        messages.success(request, "First fill the field. Please ")
        return redirect('home')
    else:
        if(request.POST['skill'] == ""):
            filter1 = json_response
        else:
            for j in json_response:
                if(j['skill'] == request.POST['skill']):
                    contain={
                        'company_name' : j['company_name'],
                        'company_address' : j['company_address'],
                        'skill' : j['skill'],
                        'salary' : j['salary'],
                        'urgent' : j['urgent']
                    }
                    filter1.append(contain) 


        if(request.POST['place'] == ""):
            filter2 = filter1
        else:
            for j in filter1:
                if(j['company_address'] == request.POST['place']):
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

from django.contrib.auth import login as django_login, logout as django_logout
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerilizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        django_login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=200)

class LogoutView(APIView):
    authentication_clasess = {TokenAuthentication}

    def post(self, request):
        django_logout(request)
        return Response(status=204)