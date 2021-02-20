from django.shortcuts import render

from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import UserForm
from .models import User


def index(request):
    """Главная страничка, подключите css плз в static/shop/style.css"""
    return render(request, 'shop/index.html')


class UserCreateView(CreateView):
    template_name = 'shop/create_user.html'
    form_class = UserForm
    success_url = reverse_lazy('index')


#def create_user(request):
#    """"Не работает))))"""
#    email = request.GET.get('email')
#   password = request.GET.get('password')
#    first_name = request.GET.get('first_name')
#    last_name = request.GET.get('last_name ')
#    User.objects.create(email=email, password=password, first_name=first_name, last_name=last_name)
#    return render(request)
