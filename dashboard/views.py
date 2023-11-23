from django.shortcuts import render,redirect
from django.conf import settings
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Case,When
from .models import InformasiKaryawan,Notifications,AdminNotifications
from authentication.models import CustomUser
from datetime import datetime
from .xlsx_utils import import_karyawan_from_xlsx
# Create your views here.


@login_required(login_url='authentication:login-form')
def main(request):
    try:
        notifikasi_personal = Notifications.objects.get(user=request.user.id,notification_type="Informasi Personal")
        context = {
            'notifikasi_personal' : notifikasi_personal,
        }
    except Notifications.DoesNotExist:
        context = {
            'detail' : "Saat ini tidak ada notifikasi yang masuk"
        }

    if request.method == "POST":
        id = request.POST.get("personalUpdateId")
        informasi_karyawan = InformasiKaryawan.objects.get(id=id)
        status = request.POST.get("status")
        pesan = request.POST.get("update_reason")
        
        if status == "Accepted":
            informasi_karyawan.status = "Accepted"
            informasi_karyawan.save()
            notifikasi_personal.delete()
            success_message = "Update karyawan telah disetujui"
            messages.success(request, success_message)
            return redirect("dashboard:main")
        
        elif status == "Declined":
            informasi_karyawan.status = "Need Revision"
            informasi_karyawan.pesan = pesan
            informasi_karyawan.save()
            notifikasi_personal.delete()
            success_message = "Update karyawan telah diberi feedback"
            messages.success(request, success_message)
            return redirect("dashboard:main")



    return render(request,"dashboard/base/main.html",context)

@login_required(login_url='authentication:login-form')
def admin_tambah_personel(request):
    # Handle form tambah personel (Admin) lewat file
    if request.method == "POST" and "personel-file" in request.FILES:
        personel_file = request.FILES['personel-file']
        if personel_file:
            try:
                import_karyawan_from_xlsx(personel_file)
            except IntegrityError:
                messages.error(request,"Nama karyawan sudah ada")
                return redirect("dashboard:tambah-personel")

            success_message = "Personel karyawan berhasil ditambahkan melalui file"
            messages.success(request, success_message)
            return redirect("dashboard:tambah-personel")
        
    # Handle form tambah personel (Admin) satu - satu
    elif request.method == "POST":
        nama = request.POST.get('nama')
        jabatan = request.POST.get('jabatan')
        status_sertifikasi = request.POST.get('status_sertifikasi')
        status_kuasa_hukum = request.POST.get('status_kuasa_hukum')
        
        try:
            izin_berlaku_attorney = datetime.strptime(request.POST.get('izin_berlaku_attorney'), "%m/%d/%Y").strftime("%Y-%m-%d")
        except TypeError or ValueError:
            izin_berlaku_attorney = None
        try:
            izin_berlaku_konsultan = datetime.strptime(request.POST.get('izin_berlaku_konsultan'), "%m/%d/%Y").strftime("%Y-%m-%d")
        except TypeError or ValueError:
            izin_berlaku_konsultan = None

        informasi_karyawan = InformasiKaryawan(
            nama=nama,
            jabatan=jabatan,
            status_sertifikasi=status_sertifikasi,
            status_kuasa_hukum=status_kuasa_hukum,
            izin_berlaku_attorney=izin_berlaku_attorney,
            izin_berlaku_konsultan=izin_berlaku_konsultan
        )
        email = nama.replace(" ","").lower() + "@ddtc.dashboard"
        user = CustomUser(
            nama=nama,
            email=email,
            password="12345",
            role="user"
        )
        
        try:
            informasi_karyawan.save()
            user.save()
        except IntegrityError:
            messages.error(request,"Nama karyawan atau email sudah ada")
            return redirect("dashboard:tambah-personel")
        
        users_notified = CustomUser.objects.filter(role="Super User")
        
        for user_notified in users_notified:
            notifikasi = Notifications(
                user=user_notified,
                informasi_karyawan=informasi_karyawan,
                notification_type="Karyawan Baru"
            )
            notifikasi.save()

        success_message = "Personel karyawan berhasil ditambahkan (Menunggu approval)"
        messages.success(request, success_message)

        return render(request,"dashboard/admin/admin-tambah-personel.html")

    return render(request,"dashboard/admin/admin-tambah-personel.html")

def user_notification(request):
    notifikasi_karyawan_baru = Notifications.objects.filter(user=request.user.id,notification_type="Karyawan Baru")
    notifikasi_jabatan_baru = Notifications.objects.filter(user=request.user.id,notification_type="Jabatan")
    notifikasi_personal = Notifications.objects.filter(user=request.user.id,notification_type="Informasi Personal")
    
    context = {
        'notifikasi_karyawan_baru' : notifikasi_karyawan_baru,
        'notifikasi_jabatan_baru' : notifikasi_jabatan_baru,
        'notifikasi_personal' : notifikasi_personal,
        'detail' : "No income notification !"
    }

    if request.method == "POST":
        status = request.POST.get('status')
        nama = request.POST.get('nama')
        pesan = request.POST.get('update_reason')

        informasi_karyawan = InformasiKaryawan.objects.get(nama=nama)
        super_user = CustomUser.objects.filter(role="Super User")
        super_user_notifikasi = Notifications.objects.filter(user__in=super_user,informasi_karyawan=informasi_karyawan)
        user_admins = CustomUser.objects.filter(role="Admin")

        if status == "Accepted" :
            for notifikasi in super_user_notifikasi:
                notifikasi.delete()
            informasi_karyawan.status = "Accepted"
            informasi_karyawan.save()
            success_message = "Personel diterima"
            messages.success(request, success_message)
            return redirect('dashboard:user-notification')
        elif status == "Declined":
            for notifikasi in super_user_notifikasi:
                notifikasi.delete()
            informasi_karyawan.delete()
            success_message = "Personel ditolak"
            messages.success(request, success_message)
            return redirect('dashboard:user-notification')
        elif status == "Requested for update":
            for notifikasi in super_user_notifikasi:
                notifikasi.status = "Requested for update"
                notifikasi.save()
            for user_admin in user_admins:
                notifikasi_admin = AdminNotifications(user=user_admin,informasi_karyawan=informasi_karyawan,pesan=pesan)
                notifikasi_admin.save()
            success_message = "Meminta perubahan"
            messages.success(request, success_message)
            return redirect('dashboard:user-notification')
 
    return render(request,"dashboard/super_user/notifikasi.html",context)
    
def admin_notifikasi(request):
    notifikasi = AdminNotifications.objects.filter(user=request.user.id)
    
    context = {
        'notifikasi' : notifikasi,
        'detail' : "Saat ini tidak ada notifikasi yang masuk"
    }

    if request.method == "POST":
        id = request.POST.get('id')
        informasi_karyawan = InformasiKaryawan.objects.get(id=id)

        informasi_karyawan.nama = request.POST.get('nama')
        informasi_karyawan.jabatan = request.POST.get('jabatan')
        informasi_karyawan.status_sertifikasi = request.POST.get('status_sertifikasi')
        informasi_karyawan.status_kuasa_hukum = request.POST.get('status_kuasa_hukum')
        informasi_karyawan.izin_berlaku_attorney = datetime.strptime(request.POST.get('izin_berlaku_attorney'), "%m/%d/%Y").strftime("%Y-%m-%d")
        informasi_karyawan.izin_berlaku_konsultan = datetime.strptime(request.POST.get('izin_berlaku_konsultan'), "%m/%d/%Y").strftime("%Y-%m-%d")
        informasi_karyawan.status = "Pending"
        users_admin = CustomUser.objects.filter(role="Admin")

        try:
            informasi_karyawan.save()
        except IntegrityError:
            messages.error(request,"Nama karyawan sudah ada")
            return redirect("dashboard:admin-notification")
        
        for user_admin in users_admin:
            admin_notifikasi = AdminNotifications.objects.get(user=user_admin,informasi_karyawan=informasi_karyawan)
            admin_notifikasi.delete()
        success_message = "Personel karyawan berhasil diperbaiki (Menunggu approval)"
        messages.success(request, success_message)
        return redirect("dashboard:admin-notification")
        
    return render(request,"dashboard/admin/admin-notifikasi.html",context)

def teams(request):

    if request.method == "POST" and "jabatan" in request.POST:
        id = request.POST.get('id')
        jabatan = request.POST.get('jabatan')

        current_karyawan = InformasiKaryawan.objects.get(id=id)

        if current_karyawan.jabatan == jabatan:
            messages.error(request,"Jabatan tidak diubah")
            return redirect("dashboard:teams")
        

        current_karyawan.jabatan = jabatan
        current_karyawan.status = "Pending"
        current_karyawan.save()
        
        users_notified = CustomUser.objects.filter(role="Super User")
        
        for user_notified in users_notified:
            notifikasi = Notifications(
                user=user_notified,
                informasi_karyawan=current_karyawan,
                notification_type="Jabatan"
            )
            notifikasi.save()
        messages.success(request,"Jabatan berhasil diedit (Menunggu approval)")
        return redirect("dashboard:teams")

    elif request.method == "POST" and "nama" in request.POST:
        id = request.POST.get('id')
        nama = request.POST.get('nama')
        status_sertifikasi = request.POST.get('status_sertifikasi')
        status_kuasa_hukum = request.POST.get('status_kuasa_hukum')
        try:
            izin_berlaku_attorney = datetime.strptime(request.POST.get('izin_berlaku_attorney'), "%m/%d/%Y").strftime("%Y-%m-%d")
        except ValueError:
            izin_berlaku_attorney = None
        except TypeError:
            izin_berlaku_attorney = None
        try:
            izin_berlaku_konsultan = datetime.strptime(request.POST.get('izin_berlaku_konsultan'), "%m/%d/%Y").strftime("%Y-%m-%d")
        except ValueError:
            izin_berlaku_konsultan = None
        except TypeError:
            izin_berlaku_konsultan = None

        current_karyawan = InformasiKaryawan.objects.get(id=id)
        user_notified = CustomUser.objects.get(nama=nama)

        current_karyawan.nama = nama
        current_karyawan.status_sertifikasi = status_sertifikasi
        current_karyawan.status_kuasa_hukum = status_kuasa_hukum
        current_karyawan.izin_berlaku_konsultan = izin_berlaku_konsultan
        current_karyawan.izin_berlaku_attorney = izin_berlaku_attorney
        current_karyawan.status = "Pending"

        try:
            current_karyawan.save()
        except IntegrityError:
            messages.error(request,"Nama karyawan sudah ada")
            return redirect("dashboard:teams")

        notifikasi = Notifications(
            user=user_notified,
            informasi_karyawan=current_karyawan,
            notification_type="Informasi Personal"
        )
        notifikasi.save()
        messages.success(request,"Informasi personel berhasil diubah (Menunggu approval)")
        return redirect("dashboard:teams")

    managers = InformasiKaryawan.objects.filter(
        jabatan__in=["Senior Manager", "Manager", "Assistant Manager"]
    ).order_by(
        Case(
            When(jabatan="Senior Manager", then=0),
            When(jabatan="Manager", then=1),
            When(jabatan="Assistant Manager", then=2),
            default=2
        )
    )
    specialists = InformasiKaryawan.objects.filter(
        jabatan__in=["Senior Specialist", "Specialist"]
    ).order_by(
        Case(
            When(jabatan="Senior Specialist", then=0),
            When(jabatan="Specialist", then=1),
            default=2
        )
    )
    admin = InformasiKaryawan.objects.filter(jabatan="Admin")

    
    content = {
        "manager" : managers,
        "specialist" : specialists,
        "admin" : admin 
    }

    return render(request,"dashboard/base/teams.html",content)

def edit_user(request):

    user = request.user

    if request.method == "POST" and "nama" in request.POST:
        print("here")
        nama = request.POST.get('nama')
        email = request.POST.get('email')

        user.nama = nama
        user.email = email
        user.save()
        
        update_session_auth_hash(request,user)
        logout(request)
        messages.success(request, "Nama dan email berhasil diubah")

        return redirect('authentication:login-form')


    elif request.method == "POST" and "oldpassword" in request.POST:
        old_password = request.POST.get('oldpassword')
        new_password = request.POST.get('newpassword')
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            logout(request)
            messages.success(request, "Password berhasil diubah")
            return redirect('authentication:login-form')
        else:
            messages.error(request, "Password lama salah")
            return redirect('dashboard:edit-user')

    content = {
        "nama" : request.user.nama,
        "email" : request.user.email
    }

    return render(request,"dashboard/base/edit-user.html",content)

