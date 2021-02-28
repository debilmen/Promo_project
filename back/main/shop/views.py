from django.contrib.auth import authenticate, login

from django.shortcuts import redirect, get_object_or_404

from django.shortcuts import render
from django.views.generic import CreateView, FormView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from .forms import RegisterForm, LoginForm, CreateCategoryForm
from .models import Categories, User


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


class CreateCategory(CreateView):
    form_class = CreateCategoryForm
    template_name = 'shop/create_category.html'
    success_url = '/categories/'

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super(CreateCategory, self).form_valid(form)



class PatchCategory:
    pass


def by_category(request):
    uid = request.user.id
    #trans = Transactions.objects.filter(category=category_id)
    categories = Categories.objects.all().filter(user_id=uid)
    context = {'categories': categories}
    return render(request, 'shop/categories.html', context)

