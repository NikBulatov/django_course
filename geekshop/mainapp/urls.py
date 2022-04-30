from django.urls import path, include
from mainapp.views import products, ProductDetail

app_name = 'mainapp'
urlpatterns = [
    path('', products, name='products'),
    path('detail/<int:pk>/', ProductDetail.as_view(), name='detail'),
    path('category/<int:id_category>/', products, name='category'),
    path('page/<int:page>/', products, name='page'),
    path('', include('social_django.urls', namespace='social'))
]
