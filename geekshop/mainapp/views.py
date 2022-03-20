from django.shortcuts import render

# Create your views here.


def index(request):  # create controller
    # request, template (path to html)
    return render(request, 'mainapp/index.html')


def products(request):
    # request, template (path to html)
    return render(request, 'mainapp/products.html')
