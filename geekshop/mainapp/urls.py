from django.urls import path, include
from mainapp.views import ProductDetail, products  # ,ProductsView

app_name = 'mainapp'
urlpatterns = [
    path('', products.as_view(), name='products'),
    # path('', ProductsView.as_view(), name='products'),
    path('detail/<int:pk>/', ProductDetail.as_view(), name='detail'),
    path('category/<int:id_category>/', products.as_view(), name='category'),
    # path('category/<int:id_category>/', ProductsView.as_view(), name='category'),
    path('page/<int:page>/', products.as_view(), name='page'),
    # path('page/<int:page>/', ProductsView.as_view(), name='page'),
    path('orders/', include('orderapp.urls', namespace='orders'))
]
