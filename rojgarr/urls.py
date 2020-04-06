from django.urls import path,include
from django.conf.urls import url
from . import views
from rest_framework import routers
from rojgarr.views import *
#from rojgarr.views import LoginView,LogoutView,Search,User_detail, Call_search
#router = routers.DefaultRouter()
#router.register('rojgarr', views.vacancies)
urlpatterns = [
    path('',views.home, name='home'),
    path('register/',views.user_detail, name='register'),
    path('header/',views.header, name='header'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login, name='login'),
    path('employer/', views.employer_part, name='employer'),
    path('employer/sign_up', views.register_employer, name='employer_sign_up'),
    path('verifylogin/',views.verified_login, name='verified_login'),
    path('create/vacancies',views.create_job, name='create_job'),
    #path('vacancies/', views.vacancies, name='vacancies'),   
    path('vacancies/<str:s>/<str:l>', views.specific_vacancy_detail, name='specific_vacancy-detail'), 
    path('search/', views.search, name='search'),
    path('userdetail/', views.user_detail, name='user_detail'),
    path('lon_lat/<str:address>',views.location_lat_lon, name='log_lat'),
    #path('Search', views.Search_Value, name='search'),
    # url(r'(?P<s>[0-9]+)/$', views.Search_Value, name='search'),
    url(r'(?P<pk>\d+)/$',views.des, name='description' ),


    path('Vacancies/', Vacancies.as_view(), name='add_vacancy'),
    # path('Search/', Call_Search.as_view(), name='start'),
    path('Catagory/<str:s>/Search_Vacancies', Search_From_Skill.as_view()),
    path('Location/<str:l>', Search_From_Location.as_view()),
    path('Search_Vacancies/Catagory/Location/<str:s>/<str:l>', Search_From_Skill_Location.as_view()),
    #path('Search/<str:skill>/<str:place>', Search.as_view()),
    path('Userdetail/', User_detail.as_view()),
    path('auth/login/', LoginView.as_view()),
    path('auth/login/', LogoutView.as_view()),
]