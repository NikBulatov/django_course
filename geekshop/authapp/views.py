from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.core.mail import message
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)  # возвращает html-код для логина, если запрос GET, форма будет пустая
        if form.is_valid():  # если форма валидна
            username = request.POST.get('username')  # берём имя
            password = request.POST.get('password')  # пароль
            user = auth.authenticate(username=username, password=password)  # если всё ок, то получим переменную user
            if user.is_active:  # если он активен
                auth.login(request, user)  # прописываем пользователя в объект запроса request.
                return HttpResponseRedirect(reverse('index'))  # Можно просто передать ей url-адрес в виде строки, а можно через reverse() вернуть адрес по его имени в диспетчере URL) Если не найдёт, то будет ошибка!
        #     else:
        #         print('Юзер не активный')
        # # else:
        # #     print(form.errors)

    else:
        form = UserLoginForm()
    context = {
        'title': 'Gekshop | Авторизация',
        'form': form
    }
    return render(request, 'authapp/login.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались')
            return HttpResponseRedirect(reverse('authapp:login'))
        else:
            print(form.errors)
    else:
        form = UserRegisterForm()
    context = {
        'title': 'Gekshop | Регистрация',
        'form': form
    }
    return render(request, 'authapp/register.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
    user_select = request.user

    context = {
        'title': 'Gekshop | Профайл',
        'form': UserProfileForm(instance=user_select),
    }

    return render(request, 'authapp/profile.html', context)


def logout(request):
    auth.logout(request)
    return render(request, 'mainapp/index.html')
