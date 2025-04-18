from django.urls import path
from user import views


urlpatterns = [
    path('profile/',views.profile,name='profile'), 
    path('profile_model/',views.profile_model,name='profile_model')
]

   
