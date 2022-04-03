import os.path
import json

from django.shortcuts import render
from mainapp.models import Product, ProductCategories

# Create your views here.
MODULE_DIR = os.path.dirname(__file__)


def read_json(path):
    data_path = os.path.join(MODULE_DIR, path)
    with open(data_path, encoding='utf-8') as f:
        items = json.load(f)
        return items


def index(request):
    content = {'title': 'GeekShop'}
    return render(request, 'mainapp/index.html', context=content)


def products(request):
    items = read_json('fixtures/items.json')
    categories = read_json('fixtures/categories.json')

    content = {
        'title': 'GeekShop - Каталог',
        'categories': ProductCategories.objects.all(),
        'items': Product.objects.all()}

    return render(request, 'mainapp/products.html', content)
