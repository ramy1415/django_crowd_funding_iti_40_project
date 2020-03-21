from django.urls import path
from django.conf.urls import url
from Users import views

app_name = 'Users'

urlpatterns=[
    path('register/',views.users_register,name='register'),
    path('login/',views.users_login,name='login'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    # path('profile/',views.user_profile,name='profile'),
    url(r'profile/',views.user_profile,name='profile')

]