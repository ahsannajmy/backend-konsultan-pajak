# Generated by Django 4.2.2 on 2023-06-14 14:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_alter_customuser_izin_berlaku'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='izin_berlaku',
            field=models.DateField(default=datetime.date.today),
        ),
    ]