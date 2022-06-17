from django.core.management.base import BaseCommand
from django.db.models import Q

from mainapp.models import ProductCategories, Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        product = Product.objects.filter(
            # Q(category__name='Обувь') & Q(id=5)  # AND
            # Q(category__name='Обувь') | Q(id=5)  # OR
            # ~Q(category__name='Обувь')  # NOT
            ~Q(category__name='Обувь'), id=5  # alternative method filtering
        )
        print(product)
