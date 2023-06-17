from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import InformasiKaryawan,Notifications,AdminNotifications
from authentication.models import CustomUser
from datetime import datetime
# Create your views here.

@login_required(login_url='authentication:login-form')
def main(request):
    return render(request,"base/main.html")

@login_required(login_url='authentication:login-form')
def admin_tambah_personel(request):
    if request.method == "POST":
        nama = request.POST.get('nama')
        jabatan = request.POST.get('jabatan')
        status_sertifikasi = request.POST.get('status_sertifikasi')
        status_kuasa_hukum = request.POST.get('status_kuasa_hukum')
        izin_berlaku_attorney = datetime.strptime(request.POST.get('izin_berlaku_attorney'), "%m/%d/%Y").strftime("%Y-%m-%d")
        izin_berlaku_konsultan = datetime.strptime(request.POST.get('izin_berlaku_konsultan'), "%m/%d/%Y").strftime("%Y-%m-%d")

        informasi_karyawan = InformasiKaryawan(
            nama=nama,
            jabatan=jabatan,
            status_sertifikasi=status_sertifikasi,
            status_kuasa_hukum=status_kuasa_hukum,
            izin_berlaku_attorney=izin_berlaku_attorney,
            izin_berlaku_konsultan=izin_berlaku_konsultan
        )
        try:
            informasi_karyawan.save()
        except IntegrityError:
            messages.error(request,"Nama karyawan sudah ada")
            return redirect("dashboard:tambah-personel")
        
        users_notified = CustomUser.objects.filter(role="Super User")
        
        for user_notified in users_notified:
            notifikasi = Notifications(
                user=user_notified,
                informasi_karyawan=informasi_karyawan,
                notification_type="Informasi Karyawan"
            )
            notifikasi.save()

        success_message = "Personel karyawan berhasil ditambahkan (Menunggu approval)"
        messages.success(request, success_message)

        return render(request,"admin/admin-tambah-personel.html")

    return render(request,"admin/admin-tambah-personel.html")

def user_notification(request):
    notifikasi = Notifications.objects.filter(user=request.user.id)

    if len(notifikasi) == 0:
        context = {
            'detail' : "Saat ini tidak ada notifikasi yang masuk"
        }
        return render(request,"notifikasi.html",context)
    
    context = {
        'notifikasi' : notifikasi
    }

    if request.method == "POST":
        status = request.POST.get('status')
        nama = request.POST.get('nama')
        pesan = request.POST.get('update_reason')

        informasi_karyawan = InformasiKaryawan.objects.get(nama=nama)
        notifikasi = Notifications.objects.get(user=request.user.id,informasi_karyawan=informasi_karyawan)
        user_admins = CustomUser.objects.filter(role="Admin")

        if status == "Accepted" :
            notifikasi.delete()
            informasi_karyawan.status = "Accepted"
            informasi_karyawan.save()
            success_message = "Personel diterima"
            messages.success(request, success_message)
            return redirect('dashboard:user-notification')
        elif status == "Declined" :
            notifikasi.delete()
            informasi_karyawan.delete()
            success_message = "Personel ditolak"
            messages.success(request, success_message)
            return redirect('dashboard:user-notification')
        elif status == "Requested for update":
            notifikasi.status = "Requested for update"
            notifikasi.save()
            for user_admin in user_admins:
                notifikasi_admin = AdminNotifications(user=user_admin,informasi_karyawan=informasi_karyawan,pesan=pesan)
                notifikasi_admin.save()
            success_message = "Meminta perubahan"
            messages.success(request, success_message)
            return redirect('dashboard:user-notification')
 
    return render(request,"super_user/notifikasi.html",context)
    
def admin_notifikasi(request):
    notifikasi = AdminNotifications.objects.filter(user=request.user.id)

    if len(notifikasi) == 0:
        context = {
            'detail' : "Saat ini tidak ada notifikasi yang masuk"
        }
        return render(request,"admin/admin-notifikasi.html",context)
    
    context = {
        'notifikasi' : notifikasi
    }

    if request.method == "POST":
        pass

    return render(request,"admin/admin-notifikasi.html",context)

def teams(request):
    partner = InformasiKaryawan.objects.filter(jabatan="Partner")
    senior_manager = InformasiKaryawan.objects.filter(jabatan="Senior Manager")
    manager = InformasiKaryawan.objects.filter(jabatan="Manager")
    asisstant_manager = InformasiKaryawan.objects.filter(jabatan="Assistant Manager")
    senior_specialist = InformasiKaryawan.objects.filter(jabatan="Senior Specialist")
    specialist = InformasiKaryawan.objects.filter(jabatan="Specialist")
    admin = InformasiKaryawan.objects.filter(jabatan="Admin")