
from .models import *
from .views import distance_calculation
from django.core.mail import EmailMessage
import schedule, time
from django.template.loader import render_to_string
from apscheduler.schedulers.background import BackgroundScheduler
#  all the above is imported class, module

# function to comparing the vacancies and profile to inform to the user
def comparing():
    intrested_user = Profile.objects.filter(recommendation = True) # filter the employee who wants the recommendation
    for n_user in intrested_user:  # loops use for email to the each user
        if n_user.address_latitude is not None and n_user.address_longitude is not None: # check the user profile have latitude and lonigute od=f his adress
            lis=[] 
            profession = n_user.profession # get user profession
            education = n_user.education # get user education
            experience = n_user.experience_year # get user experience
            vacancies1 = Vacancy_Detail.objects.filter(job_category = profession) # filter the vancies which job_categories is related with user profession
            vacancies2 = vacancies1.filter(education = education) # filter the vacncies 1 data where education is matched with education
            for vacancies3 in vacancies2: # using for loops to add the matched informsation on list
                if vacancies3.experience_year <= experience or vacancies3.experience_year is None: # condition who experience is fullfilled
                    # call the function from view which measure the distance between two places on the basic of long and lat
                    distance = distance_calculation(n_user.address_latitude,n_user.address_longitude,vacancies3.company.address_latitude,vacancies3.company.address_longitude)
                    if distance < 1.24274: # distance is obtain from miles so satisfy the condition if distance is 1.24 miles or 2 km 
                        lis.append(vacancies3) # append on list if satisfy
            if len(lis) != 0: # if list is not empty it satisy
                email = n_user.user.email # set the varaible to which the ail is to be sent
                recommend_email_user(to_email = email, lis=lis) # call the recommendation email function call

# function which helps to mail to the user of comparing is satisfy
def recommend_email_user(to_email, lis):
    subject = 'Rojgarr inform you job which are matched with your profile.'
    message = render_to_string('recommendation_email.html', {
        'lis': lis,
        })
    to_email = to_email
    email = EmailMessage(
                subject, message, to=[[to_email]]
    )
    email.send()

#  import date and time and its function
from datetime import tzinfo, timedelta, datetime

ZERO = timedelta(0)

# class use to date time format in same way between the nowdays and expiry date
class UTC(tzinfo):
  def utcoffset(self, dt):
    return ZERO
  def tzname(self, dt):
    return "UTC"
  def dst(self, dt):
    return ZERO

# function vacancies which are expired
def refine_expire_vacancies():
    import datetime
    currentDT = datetime.datetime.now(UTC()) # convert the current date according to the expiry date
    
    queryset = Vacancy_Detail.objects.select_related('company') # select query to get the company detail

    for i in queryset: # for loops is use check the whole detail optain from quey
        if(i.expiry_date.date() < currentDT.date()): # check the condition is satisfy or not
            Vacancy_Detail.objects.filter(id=i.pk).delete() # delete the vacancy which is expire

# def cronjob():
#     # schedule.every().monday.at("12:31").do(comparing) 
#     schedule.every(1).minutes.do(comparing)
#     # schedule.every().day.at("00:00").do(comparing)
#     # Loop so that the scheduling task 
#     # keeps on running all time. 
#     while True: 
    
#         # Checks whether a scheduled task  
#         # is pending to run or not 
#         schedule.run_pending() 
#         time.sleep(1) 

# function which is start to sehedule the work automaticallly after server started
def start():
    scheduler = BackgroundScheduler() # background schedular help the shedule function run on background
    scheduler.add_job(comparing, 'interval', minutes=30) # set the  comparing function on shedule accordinf minutes and repated on its interval
    scheduler.add_job(refine_expire_vacancies, 'interval', minutes=30) # set the refine_expry_function on interval to do
    scheduler.start() # recursive the same function for resheduling
    
