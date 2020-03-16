from django.urls import path
from . import views

app_name ='Projects'

urlpatterns =[
    path('',views.home_page,name='home_page')
]