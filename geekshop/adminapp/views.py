from typing import Any
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, TemplateView, CreateView
from adminapp.forms import (AdminRegisterForm,
                            AdminProfileForm,
                            ProductCreateForm,
                            ProductUpdateForm,
                            CategoryUpdateForm,
                            CategoryCreateForm)
from adminapp.mixins import BaseClassContextMixin, CustomDispatchMixin
from mainapp.models import Product, ProductCategories
from authapp.models import User


# Create your views here.


class IndexTemplateView(TemplateView, BaseClassContextMixin, CustomDispatchMixin):
    template_name = 'adminapp/admin.html'  # отдаём шаблон
    title = 'Main page'  # меняем title в контексте


class UserListView(ListView, BaseClassContextMixin, CustomDispatchMixin):
    model = User
    template_name = 'adminapp/admin-users-read.html'
    title = 'Administration | Users'
    # меняем object_list на users в контексте шаблонизатора
    context_object_name = 'users'


class UserCreateView(CreateView, BaseClassContextMixin, CustomDispatchMixin):
    model = User
    template_name = 'adminapp/admin-user-create.html'
    form_class = AdminRegisterForm  # обязательно указать форму!
    title = 'Administration | Create User'
    success_url = reverse_lazy('adminapp:admin_users')


class UserUpdateView(UpdateView, BaseClassContextMixin, CustomDispatchMixin):
    model = User
    template_name = 'adminapp/admin-user-update-delete.html'
    form_class = AdminProfileForm
    title = 'Administration | Edit Users'
    success_url = reverse_lazy('adminapp:admin_users')


class UserDeleteView(DeleteView, CustomDispatchMixin):
    model = User
    template_name = 'adminapp/admin-user-update-delete.html'
    form_class = AdminProfileForm
    success_url = reverse_lazy('adminapp:admin_users')

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.object = self.get_object()  # == User.objects.get(id=id)
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ProductsListView(ListView, BaseClassContextMixin, CustomDispatchMixin):
    model = Product
    template_name = 'adminapp/admin-products-read.html'
    title = 'Administration | Products'
    context_object_name = 'products'


class ProductDeleteView(DeleteView, CustomDispatchMixin):
    model = Product
    template_name = 'adminapp/admin-product-update-delete.html'
    form_class = ProductUpdateForm
    success_url = reverse_lazy('adminapp:admin_products')


class ProductCreateView(CreateView, BaseClassContextMixin, CustomDispatchMixin):
    model = Product
    template_name = 'adminapp/admin-product-create.html'
    form_class = ProductCreateForm
    title = 'Administration | Create Product'
    success_url = reverse_lazy('adminapp:admin_products')


class ProductUpdateView(UpdateView, BaseClassContextMixin, CustomDispatchMixin):
    model = Product
    template_name = 'adminapp/admin-product-update-delete.html'
    form_class = ProductUpdateForm
    title = 'Administration | Edit Product'
    success_url = reverse_lazy('adminapp:admin_users')


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
