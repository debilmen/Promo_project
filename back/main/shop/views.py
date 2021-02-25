from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from django.http import JsonResponse, request
from django.shortcuts import render
from django.utils.http import is_safe_url
from django.views.generic import CreateView, FormView

from .forms import RegisterForm, LoginForm

def index(request):

    """Главная страничка, подключите css плз в static/shop/style.css"""
    return render(request, 'shop/index.html')


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = '/login/'


class LoginView(FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'registration/login.html'

    def form_valid(self, form):
        request = self.request
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        return super(LoginView, self).form_invalid(form)


