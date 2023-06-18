# Generated by Django 4.2.2 on 2023-06-16 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_alter_informasikaryawan_izin_berlaku_attorney_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='informasikaryawan',
            name='status',
            field=models.CharField(choices=[('Accepted', 'Accepted'), ('Pending', 'Pending')], default='Pending', max_length=50),
        ),
        migrations.AlterField(
            model_name='informasikaryawan',
            name='nama',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]