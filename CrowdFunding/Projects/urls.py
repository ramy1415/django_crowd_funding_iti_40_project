from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'Projects'

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('projects/<int:_id>', views.project_details, name='project_details'),
    path('addprojects/', views.add_project, name='add_project'),
    path('editproject/<int:_id>',views.edit_project, name='edit_project'),
    path('projectrate/', views.project_rate, name='updateRate'),
    path('projectcomment/', views.project_comment, name='projetComment'),
    path('projects',views.all_projects,name='all_projects'),
    path('deleteimg/',views.delete_image,name='deleteimg'),
    path('addimage/',views.add_image,name='addimg'),
    path('projects', views.all_projects, name='all_projects'),
    path('projectlist/<id>', views.project_list, name='project list'),
    path('search/', views.search_projects, name='search_projects'),
    path('addreport', views.add_project_report, name='addreport'),
    path('delreport', views.del_project_report, name='delreport'),
]
