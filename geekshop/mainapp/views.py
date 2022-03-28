from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.


def index(request):
    content = {'title': 'GeekShop'}
    return render(request, 'mainapp/index.html', context=content)


def products(request):
    items = [{'name': 'Худи черного цвета с монограммами adidas Originals',
              'price': 6090,
              'description': 'Мягкая ткань для свитшотов. Стиль и комфорт – это образ жизни.'},
             {'name': 'Синяя куртка The North Face',
              'price': 23_725,
              'description': 'Гладкая ткань. Водонепроницаемое покрытие. Легкий и теплый пуховый наполнитель.'},
             {'name': 'Коричневый спортивный oversized-топ ASOS DESIGN',
              'price': 3390,
              'description': 'Материал с плюшевой текстурой. Удобный и мягкий.'},
             {'name': 'Черный рюкзак Nike Heritage',
              'price': 2340,
              'description': 'Плотная ткань. Легкий материал.'},
             {'name': 'Черные туфли на платформе с 3 парами люверсов Dr Martens 1461 Bex',
              'price': 13_590,
              'description': 'Гладкий кожаный верх. Натуральный материал.'},
             {'name': 'Темно-синие широкие строгие брюки ASOS DESIGN',
              'price': 2890,
              'description': 'Легкая эластичная ткань сирсакер Фактурная ткань.'},
             ]

    categories = [{'name': 'Новинки'},
                  {'name': 'Одежда'},
                  {'name': 'Обувь'},
                  {'name': 'Аксессуары'}]

    content = {
        'title': 'GeekShop - Каталог',
        'categories': categories,
        'items': items}

    return render(request, 'mainapp/products.html', content)
