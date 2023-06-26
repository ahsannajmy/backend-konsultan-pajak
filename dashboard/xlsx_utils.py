import openpyxl
from .models import InformasiKaryawan
from datetime import datetime
from django.db import IntegrityError
import io

def import_karyawan_from_xlsx(file):
    work_book = openpyxl.load_workbook(filename=io.BytesIO(file.read()), read_only=True)
    sheet = work_book.active

    for row in sheet.iter_rows(min_row=3):
        if row[0].value is None:
            break
        name = row[1].value
        position = row[2].value
        try:
            tax_consultant = row[3].value
        except IntegrityError:
            tax_consultant = 'Bukan Konsultan Pajak'
        try:
            expired_date_consultant = row[4].value.date()
        except AttributeError:
            expired_date_consultant = None
        try:
            tax_attorney = row[5].value
        except IntegrityError:
            tax_consultant = 'Bukan Kuasa Hukum'
        try:
            expired_date_attorney = row[6].value.date()
        except AttributeError:
            expired_date_attorney = None
        karyawan = InformasiKaryawan(
            nama=name,
            jabatan=position,
            status_sertifikasi=tax_consultant,
            status_kuasa_hukum=tax_attorney,
            izin_berlaku_attorney=expired_date_attorney,
            izin_berlaku_konsultan=expired_date_consultant,
            status="Accepted"
        )
        karyawan.save()
