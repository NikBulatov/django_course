from django.urls import path
from adminapp.views import (IndexTemplateView,

                            UserListView,
                            UserCreateView,
                            UserUpdateView,
                            UserDeleteView,

                            ProductsListView,
                            ProductCreateView,
                            ProductUpdateView,
                            ProdcutDeleteView)
from adminapp.views import (create_category, 
                            update_category, 
                            delete_category, 
                            admin_categories)

app_name = 'adminapp'
urlpatterns = [
    path('', IndexTemplateView.as_view(), name='index'),

    path('users/', UserListView.as_view(), name='admin_users'),
    path('user-create/', UserCreateView.as_view(), name='admin_users_create'),
    path('user-delete/<int:pk>/', UserDeleteView.as_view(), name='admin_users_delete'),
    path('user-update/<int:pk>/', UserUpdateView.as_view(), name='admin_users_update'),

    path('products/', ProductsListView.as_view(), name='admin_products'),
    path('product-create/', ProductCreateView.as_view(), name='create_product'),
    path('product-delete/<int:pk>/', ProdcutDeleteView.as_view(), name='delete_product'),
    path('product-update/<int:pk>/', ProductUpdateView.as_view(), name='update_product'),

    path('categories/', admin_categories, name='admin_categories'),
    path('category-create/', create_category, name='create_category'),
    path('category-delete/<int:id>/', delete_category, name='delete_category'),
    path('category-update/<int:id>/', update_category, name='update_category')]
