from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.core.mail import message
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from basket.models import Basket


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)  # возвращает html-код для логина, если запрос GET, форма будет пустая
        if form.is_valid():  # если форма валидна
            username = request.POST.get('username')  # берём имя
            password = request.POST.get('password')  # пароль
            user = auth.authenticate(username=username, password=password)  # если всё ок, то получим переменную user
            if user.is_active:  # если он активен
                auth.login(request, user)  # прописываем пользователя в объект запроса request.
                return HttpResponseRedirect(reverse(
                    'index'))  # Можно url-адрес в виде строки, а можно через reverse() вернуть адрес по его имени в диспетчере URL) Если не найдёт, то будет ошибка!
        #     else:
        #         print('Юзер не активный')
        # # else:
        # #     print(form.errors)

    else:
        form = UserLoginForm()
    context = {
        'title': 'GeekShop | Авторизация',
        'form': form
    }
    return render(request, 'authapp/login.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались!')
            return HttpResponseRedirect(reverse('authapp:login'))
        else:
            print(form.errors)
    else:
        form = UserRegisterForm()
    context = {
        'title': 'GeekShop | Регистрация',
        'form': form
    }
    return render(request, 'authapp/register.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)  # data and files для обработки и обновления данных и файлов
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные успешно обновились!')
        else:
            print(form.errors)
    user_select = request.user

    baskets = Basket.objects.filter(user=user_select)
    context = {
        'title': 'GeekShop | Профиль',
        'form': UserProfileForm(instance=user_select),  # instance - объект, с которым мы будем работать
        'baskets': baskets,
    }

    return render(request, 'authapp/profile.html', context)


@login_required
def logout(request):
    auth.logout(request)
    return render(request, 'mainapp/index.html')
