import os
import json

from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView

from mainapp.models import Product, ProductCategories

MODULE_DIR = os.path.dirname(__file__)


def read_file(name):
    file_path = os.path.join(MODULE_DIR, name)
    return json.load(open(file_path, encoding='utf-8'))


def get_link_category():
    if settings.LOW_CACHE:
        key = 'link_category'
        link_category = cache.get(key)
        if link_category is None:
            link_category = ProductCategories.objects.all()
            cache.set(key, link_category)
        return link_category
    else:
        return ProductCategories.objects.all()


def get_product_from_category(category, page):
    if settings.LOW_CACHE:
        key = f'link_product{category}{page}' if category else 'link_product'
        link_product = cache.get(key)
        if link_product is None:
            link_product = Product.objects.filter(category_id=category).select_related(
                'category') if category else Product.objects.all().select_related('category')
            cache.set(key, link_product)
        return link_product
    else:
        return Product.objects.filter(category_id=category).select_related(
            'category') if category else Product.objects.all().select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product{pk}'
        product = cache.get(key)
        if product is None:
            product = Product.objects.get(id=pk)
            cache.set(key, product)
        return product
    else:
        return Product.objects.get(id=pk)


def products(request, id_category=None, page=1):
    if id_category:
        products_ = Product.objects.filter(category_id=id_category).select_related()
        products_ = get_product_from_category(id_category, page)
    else:
        products_ = get_product_from_category(None, None)

    pagination = Paginator(products_, per_page=6)

    try:
        product_pagination = pagination.page(page)
    except PageNotAnInteger:
        product_pagination = pagination.page(1)
    except EmptyPage:
        product_pagination = pagination.page(pagination.num_pages)
    content = {
        'title': 'Geekshop - Каталог',
        # 'categories': ProductCategories.objects.all(),
        'categories': get_link_category(),
        'products': product_pagination

    }

    return render(request, 'mainapp/products.html', content)


class MainPageView(TemplateView):
    title = 'GeekShop'
    template_name = 'mainapp/index.html'


# class ProductsView(TemplateView, BaseClassContextMixin):
#     title = 'GeekShop | Catalog'
#     template_name = 'mainapp/products.html'
#
#     def get_context_data(self, id_category=None, page=1):
#         products_ = Product.objects.filter(
#             category_id=id_category).select_related() if id_category else Product.objects.all().select_related(
#             'category')  # указать по какому полю вытаскивать записи из БД
#
#         pagination = Paginator(products_, per_page=3)
#         try:
#             product_pagination = pagination.page(page)
#         except PageNotAnInteger:
#             product_pagination = pagination.page(1)
#         except EmptyPage:
#             product_pagination = pagination.page(pagination.num_pages)
#
#         context = {'categories': ProductCategories.objects.all(),
#                    'products': product_pagination}
#         return context


class ProductDetail(DetailView):
    model = Product
    template_name = 'mainapp/detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data()
        context['product'] = get_product(self.kwargs.get('pk'))
