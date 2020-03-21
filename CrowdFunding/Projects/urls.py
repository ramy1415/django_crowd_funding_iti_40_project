from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'Projects'

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('projectlist/<id>', views.project_list, name='project list'),
    path('search/', views.search_projects, name='search_projects'),
]
