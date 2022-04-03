import os.path
import json

from django.shortcuts import render

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
    items = read_json('fixtrues/items.json')
    categories = read_json('fixtrues/categories.json')

    content = {
        'title': 'GeekShop - Каталог',
        'categories': categories,
        'items': items}

    return render(request, 'mainapp/products.html', content)
