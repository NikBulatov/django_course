from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

# Create your views here.
from django.urls import reverse

from adminapp.forms import AdminRegisterForm, AdminProfileForm, ProdcutCreateForm, ProductUpdateForm, CategoryUpdateForm, CategoryCreateForm
from authapp.models import User
from mainapp.models import Product, ProductCategories


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
            print(form.errors)
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


@user_passes_test(lambda u: u.is_superuser)
def admin_products(request):
    context = {
        'title': 'Administration | Products',
        'products': Product.objects.all(),  # получить список товаров QuerySet
    }
    return render(request, 'adminapp/admin-product-read.html', context)


@user_passes_test(lambda u: u.is_superuser)
def delete_product(request, id):
    current_product = Product.objects.get(id=id)
    current_product.delete()
    messages.set_level(request, messages.SUCCESS)
    messages.success(request, 'Продукт успешно удалён')
    return HttpResponseRedirect(reverse('adminapp:delete_product'))


@user_passes_test(lambda u: u.is_superuser)
def create_product(request):
    if request.method == 'POST':
        form = ProdcutCreateForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.set_level(request, messages.SUCCESS)
            messages.success(request, 'Продукт успешно создался!')
        else:
            print(form.errors)
    else:
        form = ProdcutCreateForm()
    context = {
        'title': 'Administration | Create Product',
        'form': form
    }
    return render(request, 'adminapp/admin-product-create.html', context)


@user_passes_test(lambda u: u.is_superuser)
def update_product(request, id):
    current_product = Product.objects.get(id=id)
    if request.method == 'POST':
        form = ProductUpdateForm( data=request.POST, instance=current_product, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.set_level(request, messages.SUCCESS)
            messages.success(request, 'Продукт успешно обновился!')
        else:
            print(form.errors)
    else:
        form = ProductUpdateForm(instance=current_product)
    context = {
        'title': 'Administration | Update Product',
        'form': form,
        'current_product': current_product
    }
    return render(request, 'adminapp/admin-product-update-delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_categories(request):
    context = {
        'title': 'Administration | Categories',
        'categories': ProductCategories.objects.all()
    }
    return render(request, 'adminapp/admin-category-read.html', context)


@user_passes_test(lambda u: u.is_superuser)
def create_category(request):
    if request.method == 'POST':
        form = CategoryCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.set_level(request, messages.SUCCESS)
            messages.success(request, 'Категория успешно создалась!')
        else:
            print(form.errors)
    else:
        form = CategoryCreateForm()
    context = {
        'title': 'Administration | Create Category',
        'form': form
    }
    return render(request, 'adminapp/admin-category-create.html', context)


@user_passes_test(lambda u: u.is_superuser)
def update_category(request, id):
    current_category = ProductCategories.objects.get(id=id)
    if request.method == 'POST':
        form = CategoryUpdateForm(data=request.POST, instance=current_category)
        if form.is_valid():
            form.save()
            messages.set_level(request, messages.SUCCESS)
            messages.success(request, 'Категория успешно обновилась!')
        else:
            print(form.errors)
    else:
        form = CategoryUpdateForm(instance=current_category)
    context = {
        'title': 'Administration | Update Category',
        'form': form,
        'current_product': current_category
    }
    return render(request, 'adminapp/admin-category-read.html', context)


@user_passes_test(lambda u: u.is_superuser)
def delete_category(request, id):
    current_category = ProductCategories().objects.get(id=id)
    current_category.delete()
    messages.set_level(request, messages.SUCCESS)
    messages.success(request, 'Категория успешно удалён')
    return HttpResponseRedirect(reverse('adminapp:delete_category'))