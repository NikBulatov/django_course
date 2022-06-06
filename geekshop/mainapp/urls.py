from django.urls import path, include
from django.views.decorators.cache import cache_page

from mainapp.views import ProductDetail, products  # ,ProductsView

app_name = 'mainapp'
urlpatterns = [
    path('', cache_page(3600)(products), name='products'),
    # path('', ProductsView.as_view(), name='products'),
    path('detail/<int:pk>/', ProductDetail.as_view(), name='detail'),
    path('category/<int:id_category>/', cache_page(3600)(products), name='category'),
    # path('category/<int:id_category>/', ProductsView.as_view(), name='category'),
    path('page/<int:page>/', cache_page(3600)(products), name='page'),
    # path('page/<int:page>/', ProductsView.as_view(), name='page'),
    path('orders/', include('orderapp.urls', namespace='orders'))
]
