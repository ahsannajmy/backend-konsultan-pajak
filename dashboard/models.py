from django.db import models
from authentication.models import CustomUser

# Create your models here.
class InformasiKaryawan(models.Model):

    STATUS = (
        ('Accepted','Accepted'),
        ('Pending','Pending')
    )

    nama = models.CharField(max_length=150,unique=True)
    jabatan = models.CharField(max_length=50)
    status_sertifikasi = models.CharField(max_length=50)
    status_kuasa_hukum = models.CharField(max_length=50)
    izin_berlaku_attorney = models.DateField(default=None,null=True,blank=True)
    izin_berlaku_konsultan = models.DateField(default=None,null=True,blank=True)
    status = models.CharField(choices=STATUS,default="Pending",max_length=50)
    def __str__(self):
        return self.nama


class Notifications(models.Model):

    NOTIFICATION_TYPE = (
        ('Informasi Karyawan','Informasi Karyawan'),
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
