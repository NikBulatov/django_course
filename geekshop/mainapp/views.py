from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.


def index(request):  # create controller
    # request, template (path to html)
    return render(request, 'mainapp/index.html')


def products(request):
    return render(request, 'mainapp/products.html')


def test(request):
    context = {'title': 'geekshop',
               'header': 'Welcome',
               'user': 'Niktia',
               'products': [
                   {'name': 'Худи черного цвета с монограммами adidas Originals', 'price': 6090},
                   {'name': 'Синяя куртка The North Face', 'price': 15630},
                   {'name': 'Коричневый спортивный oversize-топ ASOS DESIGN', 'price': 3500},
                   {'name': 'Черный рюкзак Nike Heritage', 'price': 2590},
                   {'name': 'Черные туфли на платформе с 3 парами люверсов Dr Martens 1461 Bex', 'price': 3260},
                   {'name': 'Темно-синие широкие строгие брюки ASOS DESIGN', 'price': 2890},
               ],
               'promotion': False,
               'products_promotion': [
                   {'name': 'Худи черного цвета с монограммами adidas Originals', 'price': 5000},
                   {'name': 'Синяя куртка The North Face', 'price': 5000},
                   {'name': 'Коричневый спортивный oversize-топ ASOS DESIGN', 'price': 5000},
                   {'name': 'Черный рюкзак Nike Heritage', 'price': 5000},
                   {'name': 'Черные туфли на платформе с 3 парами люверсов Dr Martens 1461 Bex', 'price': 5000},
                   {'name': 'Темно-синие широкие строгие брюки ASOS DESIGN', 'price': 5000},
               ]

               }
    return render(request, 'mainapp/test.html', context=context)
