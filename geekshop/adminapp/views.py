from typing import Any
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.db import connection
from django.db.models import F
from django.db.models.signals import pre_save
from django.dispatch import receiver
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

    def get_queryset(self):
        return Product.objects.all().select_related()


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


class CategoryReadView(ListView, BaseClassContextMixin):
    model = ProductCategories
    template_name = 'adminapp/admin-category-read.html'
    title = 'Administration | Categories'
    context_object_name = 'categories'


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


class CategoryUpdateView(UpdateView, CustomDispatchMixin):
    model = ProductCategories
    template_name = 'adminapp/admin-category-update-delete.html'
    success_url = reverse_lazy('admins:admin_category')
    form_class = CategoryUpdateForm

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                print(f'Скидка {discount} % к товарам категории {self.object.name}')
                self.object.product_set.update(price=F('price') * (1 - discount / 100))
                db_profile_by_type(self.__class__, 'UPDATE', connection.queries)
        return HttpResponseRedirect(self.get_success_url())


class CategoryDeleteView(DeleteView, CustomDispatchMixin):
    model = ProductCategories
    template_name = 'adminapp/admin-category-update-delete.html'
    success_url = reverse_lazy('admins:admin_category')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.product_set.update(is_active=False)
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]


# signals
@receiver(pre_save, sender=ProductCategories)
def product_is_active_update_productcategory_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)
        db_profile_by_type(sender, 'UPDATE', connection.queries)
