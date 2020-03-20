from django.urls import path
from . import views

app_name ='Projects'

urlpatterns =[
    path('',views.home_page,name='home_page'),
    path('projects',views.all_projects,name='all_projects')
]