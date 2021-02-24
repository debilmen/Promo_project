from django.contrib.auth.views import LoginView
from django.urls import path

from .views import index

urlpatterns = [
    #path('registration/', signup, name='register'),
    path('', index, name='index'),
]