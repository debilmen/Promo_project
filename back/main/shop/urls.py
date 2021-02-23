from django.contrib.auth.views import LoginView
from django.urls import path

from .forms import UserLoginForm
from .views import index, signup

urlpatterns = [
    path('registration/', signup, name='register'),
    path('', index, name='index'),
    path('login/', LoginView.as_view(#authentication_form=UserLoginForm
     ), name='login'),
]