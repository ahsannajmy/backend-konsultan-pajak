from django.db import models
from authentication.models import CustomUser
from datetime import date

# Create your models here.
class InformasiKaryawan(models.Model):

    STATUS = (
        ('Accepted','Accepted'),
        ('Pending','Pending')
    )

    JABATAN = (
        ('Partner','Partner'),
        ('Senior Manager','Senior Manager'),
        ('Manager','Manager'),
        ('Assistant Manager','Assistant Manager'),
        ('Senior Specialist','Senior Specialist'),
        ('Specialist','Specialist'),
        ('Admin','Admin')
    )

    STATUS_SERTIFIKASI = (
        ('A','A'),
        ('B','B'),
        ('C','C'),
        ('Bukan Konsultan Pajak','Bukan Konsultan Pajak')
    )

    STATUS_KUASA_HUKUM = (
        ('Ya','Ya'),
        ('Bukan Kuasa Hukum','Bukan Kuasa Hukum')
    )
    nama = models.CharField(max_length=150,unique=True)
    jabatan = models.CharField(choices=JABATAN,max_length=50)
    status_sertifikasi = models.CharField(choices=STATUS_SERTIFIKASI,max_length=50,null=True)
    status_kuasa_hukum = models.CharField(choices=STATUS_KUASA_HUKUM,max_length=50,null=True)
    izin_berlaku_attorney = models.DateField(default=None,null=True,blank=True)
    izin_berlaku_konsultan = models.DateField(default=None,null=True,blank=True)
    status = models.CharField(choices=STATUS,default="Pending",max_length=50)

    def __str__(self):
        return self.nama
    
    @property
    def formatted_izin_berlaku_konsultan(self):
        if self.izin_berlaku_konsultan:
            return self.izin_berlaku_konsultan
        return "-"
    
    @property
    def formatted_izin_berlaku_attorney(self):
        if self.izin_berlaku_attorney:
            return self.izin_berlaku_attorney
        return "-"

    @property
    def days_until_izin_berlaku_konsultan(self):
        if self.izin_berlaku_konsultan:
            today = date.today()
            delta = self.izin_berlaku_konsultan - today
            return delta.days
        return None
    
    @property
    def days_until_izin_berlaku_attorney(self):
        if self.izin_berlaku_attorney:
            today = date.today()
            delta = self.izin_berlaku_attorney - today
            return delta.days
        return None

class Notifications(models.Model):

    # Informasi Karyawan --> Create , Delete , dan Update (Nama dan Jabatan only) untuk Super User
    # Status dan Izin --> Update (Izin berlaku dan status only) untuk User 

    NOTIFICATION_TYPE = (
        ('Karyawan Baru','Karyawan Baru'),
        ('Karyawan Keluar','Karyawan Keluar'),
        ('Jabatan','Jabatan'),
        ('Status dan Izin','Status dan Izin'),
        ('Projek','Projek')
    )

    STATUS = (
        ('Accepted','Accepted'),
        ('Declined','Declined'),
        ('Draft','Draft'),
        ('Request for update','Request for update')
    )

    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    informasi_karyawan = models.ForeignKey(InformasiKaryawan,on_delete=models.CASCADE)
    notification_type = models.CharField(choices=NOTIFICATION_TYPE,max_length=50)
    status = models.CharField(choices=STATUS,max_length=50,default='Draft')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.notification_type
    
class AdminNotifications(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    informasi_karyawan = models.ForeignKey(InformasiKaryawan,on_delete=models.CASCADE)
    pesan = models.TextField()

    def __str__(self):
        return self.pesan
