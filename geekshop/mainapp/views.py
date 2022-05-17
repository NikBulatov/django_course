import os
import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView

from adminapp.mixins import BaseClassContextMixin
from mainapp.models import Product, ProductCategories

MODULE_DIR = os.path.dirname(__file__)


def read_file(name):
    file_path = os.path.join(MODULE_DIR, name)
    return json.load(open(file_path, encoding='utf-8'))


class MainPageView(TemplateView):
    title = 'GeekShop'
    template_name = 'mainapp/index.html'


class ProductsView(TemplateView, BaseClassContextMixin):
    title = 'GeekShop | Catalog'
    template_name = 'mainapp/products.html'

    def get_context_data(self, id_category=None, page=1):
        products_ = Product.objects.filter(category_id=id_category) if id_category else Product.objects.all()

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
