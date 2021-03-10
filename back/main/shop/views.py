from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import UserPassesTestMixin

from django.shortcuts import redirect, get_object_or_404

from django.shortcuts import render
from django.views.generic import CreateView, FormView, UpdateView, DeleteView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from .forms import RegisterForm, LoginForm, CreateCategoryForm, UpdateCategoryForm
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

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(CreateCategory, self).get_form_kwargs()
        form_kwargs.update({'user_id':self.request.user})
        return form_kwargs


class UpdateCategory(UserPassesTestMixin, UpdateView):
    model = Categories
    form_class = UpdateCategoryForm
    template_name = 'shop/patch_category.html'
    success_url = '/categories'
    """Сравнивает текущее id usera с user_id Catrgories(создателя категории) и, если совпадает, то чел может редачить.
    Зачем? я не смог по другому, да и в категорию можно попасть просто вводом id категории в адресную строку
    
    А ну если true то тест проходит, и все ок, все продолжается.
    """
    def test_func(self, **kwargs):
        a = self.request.user.id
        pk = self.kwargs['pk']
        b = Categories.objects.filter(id=pk).values('user_id').first()
        if a == b['user_id']:
            return True
        else:
            raise Exception('Cant see this cuz no permissions')

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        #safe(self.request)
        return super(UpdateCategory, self).form_valid(form)

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(UpdateCategory, self).get_form_kwargs()
        form_kwargs.update({'user_id': self.request.user})
        return form_kwargs


class DeleteCategory(DeleteView):
    model = Categories
    template_name = 'shop/delete_category.html'
    success_url = '/categories'


def by_category(request):
    uid = request.user.id
    #trans = Transactions.objects.filter(category=category_id)
    categories = Categories.objects.all().filter(user_id=uid)
    context = {'categories': categories}
    return render(request, 'shop/categories.html', context)
