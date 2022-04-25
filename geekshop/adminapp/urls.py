from django.urls import path
from adminapp.views import index, admin_users, admin_users_create, admin_users_delete, admin_users_update
from adminapp.views import delete_product, create_product, admin_products, update_product
from adminapp.views import create_category, update_category, delete_category, admin_categories

app_name = 'adminapp'
urlpatterns = [
    path('', index, name='index'),
    path('users/', admin_users, name='admin_users'),
    path('user-create/', admin_users_create, name='admin_users_create'),
    path('user-delete/<int:id>/', admin_users_delete, name='admin_users_delete'),
    path('user-update/<int:id>/', admin_users_update, name='admin_users_update'),

    path('products/', admin_products, name='admin_products'),
    path('product-create/', create_product, name='create_product'),
    path('product-delete/<int:id>/', delete_product, name='delete_product'),
    path('product-update/<int:id>/', update_product, name='update_product'),

    path('categories/', admin_categories, name='admin_categories'),
    path('category-create/', create_product, name='create_category'),
    path('category-delete/<int:id>/', delete_category, name='delete_category'),
    path('category-update/<int:id>/', update_category, name='update_category')]
