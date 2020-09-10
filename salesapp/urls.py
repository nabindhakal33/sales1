from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('senddata', views.data, name='data'),
    path('update/<int:num>', views.update, name='update'),
    path('show', views.show, name='show'),
    path('delete/<int:code>', views.delete, name='delete'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
]