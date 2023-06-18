# Generated by Django 4.2.2 on 2023-06-14 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_alter_customuser_pendidikan_terakhir_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='izin_berlaku',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='jabatan',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='pendidikan_terakhir',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='status_kuasa_hukum',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='status_sertifikasi',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='username',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('User', 'User'), ('Admin', 'Admin'), ('Super User', 'Super User')], max_length=50),
        ),
    ]