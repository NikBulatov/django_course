from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

# Create your views here.
from django.urls import reverse

from adminapp.forms import AdminRegisterForm, AdminProfileForm
from authapp.models import User


@user_passes_test(lambda u: u.is_superuser)
def index(request):
    return render(request, 'adminapp/admin.html')


@user_passes_test(lambda u: u.is_superuser)
def admin_users(request):
    context = {
        'title': 'Administration | Users',
        'users': User.objects.all()  # получить список пользователей
    }
    return render(request, 'adminapp/admin-users-read.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_users_create(request):
    if request.method == 'POST':  # если отправляем данные
        form = AdminRegisterForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.set_level(request, messages.SUCCESS)
            messages.success(request, 'Пользователь успешно создался!')
            return HttpResponseRedirect(reverse('adminapp:admin_users'))
        else:
            print(form.errors)
    else:
        form = AdminRegisterForm()
    context = {'title': 'Administration | registration',
               'form': form}
    return render(request, 'adminapp/admin-users-create.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_users_update(request, id):
    current_user = User.objects.get(id=id)

    if request.method == 'POST':
        form = AdminProfileForm(data=request.POST, instance=current_user, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.set_level(request, messages.SUCCESS)
            messages.success(request, 'Данные успешно обновились!')
            return HttpResponseRedirect(reverse('adminapp:admin_users'))
    else:
        form = AdminProfileForm(instance=current_user)
    context = {
        'title': 'Administration | Update User',
        'form': form,
        'current_user': current_user
    }
    return render(request, 'adminapp/admin-users-update-delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_users_delete(request, id):  # делаем пользователя неактивным!
    current_user = User.objects.get(id=id)
    current_user.is_active = False
    current_user.save()
    return HttpResponseRedirect(reverse('adminapp:admin_users'))
