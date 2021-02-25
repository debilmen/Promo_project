from django.contrib.auth.views import LoginView
from django.urls import path

from .views import index, RegisterView,LoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('', index, name='index'),
    path('login/', LoginView.as_view(), name='login')
]