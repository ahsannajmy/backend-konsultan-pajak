# Generated by Django 4.2.2 on 2023-06-23 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_alter_informasikaryawan_jabatan_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notifications',
            name='notification_type',
            field=models.CharField(choices=[('Informasi Karyawan', 'Informasi Karyawan'), ('Status dan Izin', 'Status dan Izin'), ('Projek', 'Projek')], max_length=50),
        ),
    ]