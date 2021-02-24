from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from django.http import JsonResponse
from django.shortcuts import render


def index(request):

    """Главная страничка, подключите css плз в static/shop/style.css"""
    return render(request, 'shop/index.html')

"""""
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=email, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})

#def create_user(request):
#    """"Не работает))))"""
#    email = request.GET.get('email')
#   password = request.GET.get('password')
#    first_name = request.GET.get('first_name')
#    last_name = request.GET.get('last_name ')
#    User.objects.create(email=email, password=password, first_name=first_name, last_name=last_name)
#    return render(request)
