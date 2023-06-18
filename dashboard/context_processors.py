from .models import Notifications,AdminNotifications,InformasiKaryawan
from django.db import IntegrityError

def notification(request):

    if request.user.is_authenticated:
        if request.user.role == "Admin":
            number_of_admin_notifications = AdminNotifications.objects.filter(user=request.user.id)

            return {
                'number_of_admin_notifications' : len(number_of_admin_notifications)
            }

    number_of_notifications = Notifications.objects.filter(user=request.user.id,is_read=False)

    return {
        'number_of_notifications' : len(number_of_notifications)
    }

def user_information(request):

    if request.user.is_authenticated:
        user = request.user
        return {
            'nama' : user.nama,
            'role' : user.role
        }
    
    return {}

def user_license(request):

    if request.user.is_authenticated:
        try:
            informasi_karyawan = InformasiKaryawan.objects.get(nama=request.user.nama)
            return {
                'izin_berlaku_attorney' : informasi_karyawan.days_until_izin_berlaku_attorney,
                'izin_berlaku_konsultan' : informasi_karyawan.days_until_izin_berlaku_konsultan
            }
        except IntegrityError:
            return {
                'information' : 'Ada ketidaksesuain antara nama pengguna dengan nama di tim kontak admin untuk mengubahnya!'
            }
            
    return {}

    
    