# Generated by Django 4.2.2 on 2023-06-27 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0013_alter_informasikaryawan_status_kuasa_hukum_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notifications',
            name='notification_type',
            field=models.CharField(choices=[('Karyawan Baru', 'Karyawan Baru'), ('Karyawan Keluar', 'Karyawan Keluar'), ('Jabatan', 'Jabatan'), ('Informasi Personel', 'Informasi Personel'), ('Projek', 'Projek')], max_length=50),
        ),
    ]
