from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from django.http import JsonResponse, request
from django.shortcuts import render
from django.utils.http import is_safe_url
from django.views.generic import CreateView, FormView, RedirectView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from .forms import RegisterForm, LoginForm
from .models import Categories, Transactions


def index(request):
    """Главная страничка, подключите css плз в static/shop/style.css"""
    return render(request, 'shop/index.html')


class RegisterView(CreateView):
    """Регистрация пользователя"""
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = '/login/'


class LoginView(FormView):
    """Вход"""
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


class LogoutView(BaseLogoutView):
    next_page = 'index'


class CreateCategory:
    pass


class PatchCategory:
    pass


def by_category(request):

    user_id = request.GET.get('user.id')
    #trans = Transactions.objects.filter(category=category_id)
    categories = Categories.objects.filter(user_id=user_id)
    if categories is None:
        return render(request, 'shop/categories.html')
    else:
        return render(request, 'shop/categories.html', {'categories': categories})

