from django.urls import path,include
from django.conf.urls import url
from . import views
from rest_framework import routers
from rojgarr.views import *
from django.contrib.auth import views as auth_views

#from rojgarr.views import LoginView,LogoutView,Search,User_detail, Call_search
#router = routers.DefaultRouter()
#router.register('rojgarr', views.vacancies)
urlpatterns = [
    # home pgae without logged in for normal user
    path('',views.home, name='home'),
    # home page after logged in for normal user
    path('verified/home/',views.home_logged_in, name='log_in_home'),
    # redirected page after log in employer
    path('verified_employer/', views.login_employer, name='employer_logged_in'),

    # path for register the detail of user
    path('register/',views.user_detail, name='register'),
    path('employer/register/',views.employer_user_detail, name='employer_register'),

    # redirect page to company review
    path('all_company_reviews/',views.all_company_reviews, name='all_company_reviews'),
    path('comapny_review/',views.company_review, name='company_review'),
    url(r'view_company_review_detail/(?P<pk>\d+)/$',views.description_comapny_review, name='description_comapny_review' ),
    path('review/save', views.company_review_by_user, name='company_review_by_user'),

    # path('header/',views.header, name='header'),
    path('signup/',views.signup,name='signup'),
    # url(r'^register/$', RegisterView.as_view(), name='register'),

    path('login/',views.login_employe, name='login'),
    path('employer/', views.employer_part, name='employer'),
    path('employer/sign_up', views.register_employer, name='employer_sign_up'),

    path('logout/employe',views.logout_employe, name='logout_employe'),
    path('logout/employer',views.logout_employer, name='logout_employer'),

        # path for add the vacancy detail
    path('add_vacancy/', views.add_vacancy_detail, name='announce_vacancy'),

    # url for verify normal user login 
    # path('verifylogin/',views.verified_login, name='verified_login'),
    # url for employer verify log in
    # path('employer/verifylogin/',views.employer_verified_login, name='employer_verified_login'),
    
    # create job url
    # path('create/vacancies',views.create_job, name='create_job'),

    #path('vacancies/', views.vacancies, name='vacancies'),
    # 
    #Use of dynamic url for specific vacancie detail
    path('vacancies/<str:s>/<str:l>', views.specific_vacancy_detail, name='specific_vacancy-detail'), 
    path('search/', views.search, name='search'),
    path('userdetail/', views.user_detail, name='user_detail'),

    # url for sign up employer
    path('employer/userdetail/', views.employer_user_detail, name='employer_user_detail'),

    path('lon_lat/<str:address>',views.location_lat_lon, name='log_lat'),
    #path('Search', views.Search_Value, name='search'),
    # url(r'(?P<s>[0-9]+)/$', views.Search_Value, name='search'),
    url(r'view_detail/(?P<pk>\d+)/$',views.des, name='description' ),
    url(r'apply_job/(?P<pk>\d+)/$',views.confirmation_to_apply, name='apply_job' ),



    # path('Vacancies/', Vacancies.as_view(), name='add_vacancy'),

    # path('Search/', Call_Search.as_view(), name='start'),
    path('Catagory/<str:s>/Search_Vacancies', Search_From_Skill.as_view()),
    path('Location/<str:l>', Search_From_Location.as_view()),
    path('Search_Vacancies/Catagory/Location/<str:s>/<str:l>', Search_From_Skill_Location.as_view()),
    #path('Search/<str:skill>/<str:place>', Search.as_view()),
    path('Userdetail/', User_detail.as_view()),
    # path('auth/login/', LoginView.as_view()),
    # path('auth/login/', LogoutView.as_view()),

    # roue for the email activation
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    # path for the redirect to user page
    path('normaluser/profile', views.user_profile, name='user_profile'),
    path('edit/profile', views.edit_profile, name='edit_profile'),
]