from django.urls import path
from orderapp.views import (OrderListView,
                            OrderCreateView,
                            OrderUpdateView,
                            OrderReadView,
                            OrderDeleteView,
                            order_forming_complete,
                            get_product_price)

app_name = 'orderapp'
urlpatterns = [
    path('', OrderListView.as_view(), name='list'),
    path('create/', OrderCreateView.as_view(), name='create'),
    path('update/<int:pk>/', OrderUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', OrderDeleteView.as_view(), name='delete'),
    path('read/<int:pk>/', OrderReadView.as_view(), name='read'),
    path('forming_complete/<int:pk>/', order_forming_complete, name='order_forming_complete'),
    path('product/<int:pk>/price/', get_product_price, name='product_price'),

]
