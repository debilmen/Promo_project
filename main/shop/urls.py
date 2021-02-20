from django.urls import path
from .views import index, UserCreateView

urlpatterns = [
    path('join/', UserCreateView.as_view(), name='add'),
    path('', index, name='index'),
]