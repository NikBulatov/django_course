import os
import json
import random

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, DetailView

from adminapp.mixins import BaseClassContextMixin
from mainapp.models import Product, ProductCategories
from django.conf import settings
from django.core.cache import cache

MODULE_DIR = os.path.dirname(__file__)


def read_file(name):
    file_path = os.path.join(MODULE_DIR, name)
    return json.load(open(file_path, encoding='utf-8'))


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategories.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategories.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategories, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategories, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_ordered_by_price():
    if settings.LOW_CACHE:
        key = 'get_products_ordered_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).order_by('price')


def get_products_in_category_ordered_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_ordered_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by(
                'price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')


def get_hot_product():
    products = get_products()
    return random.sample(list(products), 1)[0]


class MainPageView(TemplateView):
    title = 'GeekShop'
    template_name = 'mainapp/index.html'


class ProductsView(TemplateView, BaseClassContextMixin):
    title = 'GeekShop | Catalog'
    template_name = 'mainapp/products.html'

    def get_context_data(self, id_category=None, page=1):
        products_ = get_products()

        pagination = Paginator(products_, per_page=3)
        try:
            product_pagination = pagination.page(page)
        except PageNotAnInteger:
            product_pagination = pagination.page(1)
        except EmptyPage:
            product_pagination = pagination.page(pagination.num_pages)

        context = {'categories': ProductCategories.objects.all(),
                   'products': product_pagination}
        return context


class ProductDetail(DetailView):
    model = Product
    template_name = 'mainapp/detail.html'
