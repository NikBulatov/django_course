from django.test import TestCase  # Smoke tests the same. It doesn't change data in DB

# Create your tests here.
from mainapp.models import ProductCategories, Product
from django.test.client import Client


class TestMainApp(TestCase):  # класс необязательно именовать с Test, а методы обязательно
    def setUp(self) -> None:  # prepare
        category = ProductCategories.objects.create(name='Test')
        Product.objects.create(category=category, name='product_1', price=150_000)
        self.client = Client()

    def tearDown(self) -> None:  # clear after test
        pass

    def test_product_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_product(self):
        for item in Product.objects.all():
            response = self.client.get(f'/products/detail/{item.pk}/')
            self.assertEqual(response.status_code, 200)
