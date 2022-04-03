from django.contrib import admin
from mainapp.models import Product, ProductCategories

# Register your models here.
admin.site.register(ProductCategories)
admin.site.register(Product)
