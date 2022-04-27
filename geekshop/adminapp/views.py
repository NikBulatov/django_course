from http.client import HTTPResponse
from typing import Any
from django.contrib import messages
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from adminapp.forms import AdminRegisterForm, AdminProfileForm, ProdcutCreateForm, ProductUpdateForm, CategoryUpdateForm, CategoryCreateForm
from authapp.models import User
from adminapp.mixin import BaseClassContextMixin, CustomDispatchMixin
from mainapp.models import Product, ProductCategories
from django.views.generic import ListView, UpdateView, DetailView, DeleteView, TemplateView, CreateView
# Create your views here.


# @user_passes_test(lambda u: u.is_superuser)
# def index(request):
#     return render(request, 'adminapp/admin.html')


# класс для рендеринга html. Базовый класс в mixin
# Так делать не очень
class IndexTemplateView(TemplateView, BaseClassContextMixin, CustomDispatchMixin):
    template_name = 'adminapp/admin.html'  # отдаём шаблон
    title = 'Main page'  # меняем title в контексте

    # @method_decorator(user_passes_test(lambda u: u.is_superuser))  #
    # def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:  # можем переопределить метод для обработки рендера
    #     return super(IndexTemplateView).dispatch(request, *args, **kwargs)

    # def get_context_data(self, **kwargs):
    #     context = super(IndexTemplateView, self).get_context_data(**kwargs)
    #     context['title'] = 'title'
    #     return context


class UserListView(ListView, BaseClassContextMixin, CustomDispatchMixin):
    model = User
    template_name = 'adminapp/admin-users-read.html'
    title = 'Administration | Users'
    # меняем object_list на users в контексте шаблонизатора
    context_object_name = 'users'


@user_passes_test(lambda u: u.is_superuser)
def admin_users(request):
    context = {
        'title': 'Administration | Users',
        'users': User.objects.all()  # получить список пользователей
    }
    return render(request, 'adminapp/admin-users-read.html', context)


class UserCreateView(CreateView, BaseClassContextMixin, CustomDispatchMixin):
    model = User
    template_name = 'adminapp/admin-users-create.html'
    form_class = AdminRegisterForm  # обязательно указать форму!
    title = 'Administration | Create User'
    success_url = reverse_lazy('adminapp:admin_users')

    # def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
    #     return super().post(request, *args, **kwargs)

    # def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
    #     return super().get(request, *args, **kwargs)

    # def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
    #     return super().get_context_data(**kwargs)

# @user_passes_test(lambda u: u.is_superuser)
# def admin_users_create(request):
#     if request.method == 'POST':  # если отправляем данные
#         form = AdminRegisterForm(data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.set_level(request, messages.SUCCESS)
#             messages.success(request, 'Пользователь успешно создался!')
#             return HttpResponseRedirect(reverse('adminapp:admin_users'))
#         else:
#             print(form.errors)
#     else:
#         form = AdminRegisterForm()
#     context = {'title': 'Administration | registration',
#                'form': form}
#     return render(request, 'adminapp/admin-users-create.html', context)


class UserUpdateView(UpdateView, BaseClassContextMixin, CustomDispatchMixin):
    model = User
    template_name = 'adminapp/admin-users-update-delete.html'
    form_class = AdminProfileForm
    title = 'Administration | Edit Users'
    success_url = reverse_lazy('adminapp:admin_users')

# @user_passes_test(lambda u: u.is_superuser)
# def admin_users_update(request, id):
#     current_user = User.objects.get(id=id)

#     if request.method == 'POST':
#         form = AdminProfileForm(
#             data=request.POST, instance=current_user, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.set_level(request, messages.SUCCESS)
#             messages.success(request, 'Данные успешно обновились!')
#             return HttpResponseRedirect(reverse('adminapp:admin_users'))
#         else:
#             print(form.errors)
#     else:
#         form = AdminProfileForm(instance=current_user)
#     context = {
#         'title': 'Administration | Update User',
#         'form': form,
#         'current_user': current_user
#     }
#     return render(request, 'adminapp/admin-users-update-delete.html', context)


class UserDeleteView(DeleteView, CustomDispatchMixin):
    model = User
    template_name = 'adminapp/admin-users-update-delete.html'
    form_class = AdminProfileForm
    success_url = reverse_lazy('adminapp:admin_users')

    # def delete(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
    #     return super().delete(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HTTPResponse:
        self.object = self.get_object()  # == User.objects.get(id=id)
        self.get_object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


# @user_passes_test(lambda u: u.is_superuser)
# def admin_users_delete(request, id):  # делаем пользователя неактивным!
#     current_user = User.objects.get(id=id)
#     current_user.is_active = False
#     current_user.save()
#     return HttpResponseRedirect(reverse('adminapp:admin_users'))


@user_passes_test(lambda u: u.is_superuser)
def admin_products(request):
    context = {
        'title': 'Administration | Products',
        'products': Product.objects.all()  # получить список товаров QuerySet
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
        form = ProductUpdateForm(
            data=request.POST, instance=current_product, files=request.FILES)
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
