from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'app'

urlpatterns = [
    #basic
    path('',
         views.home, name='home'),
    #login/registration/logout
    path('login/',
         auth_views.login, {'template_name': 'account/access_account/login.html'}, name='login'),
    path('logout/',
         auth_views.logout, {'template_name': 'account/access_account/logout.html'}, name='logout'),
    path('signup/',
         views.signup, name='signup'),
    #account
    path('accounts/profile/',
         views.profile, name='profile'),
    path('accounts/profile_new_entry/',
         views.profile_new_entry, name='profile_new_entry'),
    path('accounts/profile/profile_object_edit/<int:pk>/',
         views.profile_object_edit, name='profile_object_edit'),
    path('accounts/profile/profile_object_delete/<int:pk>/',
         views.profile_object_delete, name='profile_object_delete'),
    path('accounts/profile/profile_password_shared/<int:pk>/',
         views.profile_password_shared, name='profile_password_shared'),
    #passwor get
    path('password_get/<forwarding>/',
         views.password_get, name='password_get')
]