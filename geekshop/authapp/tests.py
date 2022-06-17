from django.conf import settings
from django.test import TestCase

# Create your tests here.
from authapp.models import User
from mainapp.models import ProductCategories, Product
from django.test.client import Client


class TestAuthApp(TestCase):
    def setUp(self) -> None:
        self.username = 'django'
        self.useremail = 'django@mail.ru'
        self.password = '1234567890'

        self.new_user_data = {
            'username': 'django',
            'first_name': 'django1',
            'last_name': 'django1',
            'email': 'django1@mail.ru',
            'password1': '1234567890',
            'password2': '1234567890',
            'age': 32
        }
        self.user = User.objects.create_superuser(self.username, self.useremail, self.password)
        category = ProductCategories.objects.create(name='Test')
        Product.objects.create(category=category, name='product_1', price=150_000)
        self.client = Client()

    def tearDown(self) -> None:  # clear after test
        pass

    def test_login_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/authapp/profile/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/authapp/profile/')
        self.assertEqual(response.status_code, 200)

    def test_registered(self):
        response = self.client.post('/authapp/register/', data=self.new_user_data)
        self.assertEqual(response.status_code, 200)

        user = User.objects.get(username=self.new_user_data['username'])

        activation_url = f'{settings.DOMAIN_NAME}/authapp/verify/{user.email}/{user.activation_key}/'
        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(user.is_active)
        user.refresh_from_db()
        self.assertTrue(user.is_active)
