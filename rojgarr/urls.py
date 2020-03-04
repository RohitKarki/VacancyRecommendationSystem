from django.urls import path,include
from . import views
from rest_framework import routers
from rojgarr.views import Vacancies,LoginView,LogoutView,Search,UserDetail

#router = routers.DefaultRouter()
#router.register('rojgarr', views.vacancies)
urlpatterns = [
    path('',views.home, name='home'),
    path('register/',views.user_detail, name='register'),
    path('header/',views.header, name='header'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login, name='login'),
    path('verifylogin/',views.verified_login, name='verified_login'),
    #path('vacancies/', views.vacancies, name='vacancies'),   
    path('vacancies/<int:pk>/', views.specific_vacancy_detail, name='specific_vacancy-detail'), 
    path('search/', views.search, name='search'),
    path('userdetail/', views.user_detail, name='user_detail'),
    # #path('',include(router.urls)),


    path('Vacancies/', Vacancies.as_view()),
    path('Search/<str:place>/<str:skill>', Search.as_view()),
    path('Userdetail/', UserDetail.as_view()),
    path('auth/login/', LoginView.as_view()),
    path('auth/login/', LogoutView.as_view()),
]