# Generated by Django 4.2.2 on 2023-06-16 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_notifications_informasi_karyawan'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='status',
            field=models.CharField(choices=[('Accepted', 'Accepted'), ('Declined', 'Declined'), ('Draft', 'Draft'), ('Request for update', 'Request for update')], default='Draft', max_length=50),
        ),
    ]