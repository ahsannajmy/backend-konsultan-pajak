from django.contrib import admin
from .models import InformasiKaryawan,Notifications,AdminNotifications
# Register your models here.
admin.site.register(InformasiKaryawan)
admin.site.register(Notifications)
admin.site.register(AdminNotifications)