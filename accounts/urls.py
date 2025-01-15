from django.contrib import admin
from django.urls import path , include
from . import views
urlpatterns = [
    path('register/' , views.register , name= 'register'),
    path('signin/' , views.signin , name='signin'),
    path('logout/' , views.logout , name='logout'),
    path('activate/<uidb64>/<token>/' , views.activate , name='activate'),
    path('' , views.dashboard , name='dashboard'),
    path('dashboard/' , views.dashboard , name='dashboard'),
    path('forgotPassword/' , views.forgot_password , name='forgot_password'),
    path('reset_password_validate/<udidb64>/<token>' , views.reset_password_validate , name='reset_password_validate'),
    path('resetPassword/' , views.reset_password , name='reset_password'),

]
