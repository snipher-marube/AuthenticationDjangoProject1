from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.loginuser, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('set-new-password/<uidb64>/<token>/', views.password_reset_confirm, name='set-new-password'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

]
