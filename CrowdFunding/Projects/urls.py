from django.urls import path
from . import views

app_name = 'Projects'


urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('projects/<int:_id>', views.project_details, name='project_details'),
    path('addprojects/', views.add_project, name='add_project'),
    path('projectrate/', views.project_rate, name='updateRate'),
    path('projectcomment/', views.project_comment, name='projetComment'),
    path('projects',views.all_projects,name='all_projects')
]

