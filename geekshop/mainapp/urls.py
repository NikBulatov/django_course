from django.urls import path, include
from django.views.decorators.cache import cache_page

from mainapp.views import ProductDetail, products

app_name = 'mainapp'
urlpatterns = [
    path('', products, name='products'),
    path('detail/<int:pk>/', ProductDetail.as_view(), name='detail'),
    path('category/<int:id_category>/', products, name='category'),
    path('page/<int:page>/', products, name='page'),
    path('orders/', include('orderapp.urls', namespace='orders'))
]
