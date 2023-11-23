from django.db import models
from authentication.models import CustomUser


# Create your models here.
class Project:
    JENIS_PROJECT = (
        ('Audit','Audit'),
        ('Objection','Objection'),
        ('Appeal','Appeal'),
        ('Lawsuit','Lawsuit'),
        ('Judicial Review','Compliance'),
        ('Others','Others')
    )
    JENIS_TAX = (
        ('VAT','VAT'),
        ('WHT 21','WHT 21'),
        ('WHT 22','WHT 22'),
        ('WHT 23','WHT 23'),
        ('WHT 26','WHT 26'),
        ('WHT 4(2)','WHT 4(2)'),
        ('CIT','CIT'),
        ('Others','Others')
    )
    MONTH = (
        ('January','January'),
        ('February','February'),
        ('March','March'),
        ('April','April'),
        ('May','May'),
        ('June','June'),
        ('July','July'),
        ('August','August'),
        ('September','September'),
        ('October','October'),
        ('November','November'),
        ('December','December')
    )
    client = models.CharField(max_length=512)
    jenis_project = models.CharField(choices=JENIS_PROJECT)
    jenis_tax = models.CharField(choices=JENIS_TAX)
    periode_awal = models.CharField(choices=MONTH)
    periode_akhir = models.CharField(choices=MONTH)
    fiscal_year = models.CharField(max_length=512)
    PIC = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    MEMBER = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    value = models.BigIntegerField()
    
