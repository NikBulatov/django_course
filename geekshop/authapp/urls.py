from django.urls import path

from authapp.views import login, register
from authapp.views import Logout, ProfileFormView, Login, RegisterFormView

app_name = 'authapp'
urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('register/', RegisterFormView.as_view(), name='register'),
    path('profile/', ProfileFormView.as_view(), name='profile'),
    path('logout/', Logout.as_view(), name='logout'),
    path('verify/<str:email>/<str:activate_key>/', RegisterFormView.verify, name='verify')
]
