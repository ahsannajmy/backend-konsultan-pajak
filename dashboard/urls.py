from django.urls import path
from .views import main,admin_tambah_personel,user_notification,admin_notifikasi


app_name = 'dashboard'
urlpatterns = [
    path('',main,name='main'),
    path('notifikasi/',user_notification,name='user-notification'),
    path('admin/tambah-personel/',admin_tambah_personel,name='tambah-personel'),
    path('admin/notifikasi',admin_notifikasi,name='admin-notification')
]