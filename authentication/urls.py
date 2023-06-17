from django.urls import path
from .views import login,register,logout_view


app_name = 'authentication'
urlpatterns = [
    path('login/',login,name='login-form'),
    path('register/',register,name='register'),
    path('logout/',logout_view,name='logout')
]