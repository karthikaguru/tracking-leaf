from django.contrib import admin
from django.urls import path
from frontsite import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/',views.register,name='register'),

  #  path('client/<int:client_id>/', views.client_details, name='client_details'),
    path('client/<int:id>/update/', views.client_update, name='client_update'),
  #  path('client/<int:client_id>/delete/', views.client_delete_view, name='client_delete'),
    path('clients/', views.client_list, name='client_list'),
    path('',views.login_view,name='login'),
    path('logout',views.logout_view,name='logout'),
    path('index/',views.index,name= 'index'),
    path('contactus/',views.contact_us,name='contactus'),
     path('about/', views.about_us, name='about'), 
]

   
