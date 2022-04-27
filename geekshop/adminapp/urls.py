from django.urls import path
from adminapp.views import UserCreateView, IndexTemplateView, UserListView, UserUpdateView, UserDeleteView
from adminapp.views import delete_product, create_product, admin_products, update_product
from adminapp.views import create_category, update_category, delete_category, admin_categories

app_name = 'adminapp'
urlpatterns = [
    path('', IndexTemplateView.as_view(), name='index'),
    path('users/', UserListView.as_view(), name='admin_users'),
    path('user-create/', UserCreateView.as_view(), name='admin_users_create'),
    path('user-delete/<int:pk>/', UserDeleteView.as_view(), name='admin_users_delete'),
    path('user-update/<int:pk>/', UserUpdateView.as_view(), name='admin_users_update'),

    path('products/', admin_products, name='admin_products'),
    path('product-create/', create_product, name='create_product'),
    path('product-delete/<int:id>/', delete_product, name='delete_product'),
    path('product-update/<int:id>/', update_product, name='update_product'),

    path('categories/', admin_categories, name='admin_categories'),
    path('category-create/', create_category, name='create_category'),
    path('category-delete/<int:id>/', delete_category, name='delete_category'),
    path('category-update/<int:id>/', update_category, name='update_category')]
