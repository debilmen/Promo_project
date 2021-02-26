from django.contrib.auth.views import LoginView
from django.urls import path

from .views import index, RegisterView,LoginView, LogoutView, by_category

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('', index, name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('categories/', by_category, name='get_categories')
]