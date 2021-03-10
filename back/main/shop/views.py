from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import UserPassesTestMixin

from django.shortcuts import redirect, get_object_or_404

from django.shortcuts import render
from django.template.loader import get_template
from django.views.generic import CreateView, FormView, UpdateView, DeleteView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from .forms import RegisterForm, LoginForm, CategoryForm, TransactionForm

from .models import Categories, User, Transactions


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


class GetCategories:
    def __init__(self):
        self.user = User.objects

    def by_category(self):
        uid = self.user.id

        categories = Categories.objects.all().filter(user_id=uid)
        context = {'categories': categories}
        return render(self, 'shop/categories/categories.html', context)


class CreateCategory(CreateView):
    form_class = CategoryForm
    template_name = 'shop/categories/create_category.html'
    success_url = '/categories/'

    def form_valid(self, form):
        form.instance.user_id = self.request.user

        return super(CreateCategory, self).form_valid(form)

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(CreateCategory, self).get_form_kwargs()

        form_kwargs.update({'user_id': self.request.user})
        return form_kwargs


class UpdateCategory(UserPassesTestMixin, UpdateView):
    model = Categories
    form_class = CategoryForm
    template_name = 'shop/categories/patch_category.html'
    success_url = '/categories'



    """Сравнивает текущее id usera с user_id Catrgories(создателя категории) и, если совпадает, то чел может редачить.
      Зачем? я не смог по другому, да и в категорию можно попасть просто вводом id категории в адресную строку

      А ну если true то тест проходит, и все ок, все продолжается.
      """
    def test_func(self, **kwargs):
        pk = self.kwargs['pk']
        b = Categories.objects.get(id=pk).user_id.id
        if self.request.user.id == b:
            return True
        else:
            raise Exception(b, ' 96 view', 'u cant see this, permissiondeniead')

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
    template_name = 'shop/delete.html'
    success_url = '/categories'


class GetTransaction:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user = User.objects

    def get_transactions(self):
            uid = self.user.id
            trans = Transactions.objects.filter(user_id=uid)
            context = {'transactions': trans}
            return render(self, 'shop/transactions/transactions.html', context)

    def info_transaction(self, pk):
        uid = self.user.id
        trans = Transactions.objects.filter(id=pk, user_id=uid)
        categories = Categories.objects.filter(id=12)
        context = {'transactions': trans,
                   'categories': categories}
        return render(self, 'shop/transactions/info_transaction.html', context)


class CreateTransaction(CreateView):
    form_class = TransactionForm
    template_name = 'shop/transactions/create_transaction.html'
    success_url = '/transactions/'

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super(CreateTransaction, self).form_valid(form)

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(CreateTransaction, self).get_form_kwargs()
        form_kwargs.update({'user_id': self.request.user})
        #form_kwargs.update({'query': Categories.objects.get(user_id=self.request.user)})
        return form_kwargs


class UpdateTransaction(UserPassesTestMixin,UpdateView):
    model = Transactions
    form_class = TransactionForm
    template_name = 'shop/transactions/create_transaction.html'
    success_url = '/transactions/'

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super(UpdateTransaction, self).form_valid(form)

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(UpdateTransaction, self).get_form_kwargs()
        form_kwargs.update({'user_id': self.request.user})
        #form_kwargs.update({'query': Categories.objects.get(user_id=self.request.user)})
        return form_kwargs

    def test_func(self, **kwargs):
        pk = self.kwargs['pk']
        b = Transactions.objects.get(id=pk).user_id.id
        if self.request.user.id == b:
            return True
        else:
            raise Exception(b, ' 96 view')

class DeleteTransaction(DeleteView):
    model = Transactions
    template_name = 'shop/delete.html'
    success_url = '/transactions/'
