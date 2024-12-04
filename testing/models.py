import json
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Bidang(models.Model):
    id = models.AutoField(primary_key=True)
    nama = models.CharField(max_length=255)

    def __str__(self):  # Nama method harus __str__ (dua garis bawah di kiri dan kanan)
        return self.nama
    
    class Meta:
        verbose_name_plural = "Bidang"
        ordering = ['id']

class Pegawai(models.Model):
    id = models.AutoField(primary_key=True)  # ID otomatis
    nomor_induk = models.CharField(max_length=20, unique=True)  # Nomor induk pegawai
    nama = models.CharField(max_length=100)  # Nama pegawai
    alamat = models.TextField()  # Alamat pegawai
    no_telp = models.CharField(max_length=15)  # Nomor telepon pegawai
    bidang = models.ForeignKey(Bidang, on_delete=models.CASCADE)  # Relasi ke tabel Bidang

    def __str__(self):
        return f"{self.nama} - {self.nomor_induk}"
    
    class Meta:
        verbose_name_plural = "Pegawai"
        ordering = ['nama']
        
class Kriteria(models.Model):
    TIPE_CHOICES = [
        ('benefit', 'Benefit'),
        ('cost', 'Cost'),
    ]

    id = models.AutoField(primary_key=True)  # ID otomatis
    nama = models.CharField(max_length=100)  # Nama kriteria
    bobot = models.FloatField(default=0, null=False, blank=False)  # Bobot, default 0
    tipe = models.CharField(max_length=10, choices=TIPE_CHOICES, default='benefit')  # Tipe kriteria (Benefit/Cost)

    def __str__(self):
        return f"{self.nama} (Bobot: {self.bobot}, Tipe: {self.get_tipe_display()})"
    
    class Meta:
        verbose_name_plural = "Kriteria"
        ordering = ['nama']  # Urutkan berdasarkan nama secara default
    
class Penilaian(models.Model):
    id = models.AutoField(primary_key=True)  # ID otomatis
    nama = models.ForeignKey('Pegawai', on_delete=models.CASCADE)  # Relasi ke tabel Pegawai
    bidang = models.ForeignKey('Bidang', on_delete=models.CASCADE)  # Relasi ke tabel Bidang
    nilai = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Penilaian {self.nama.nama} - {self.bidang.nama}"
    
    class Meta:
        verbose_name_plural = "Penilaian"
        ordering = ['id']
        
class PegawaiTerbaik(models.Model):
    id = models.AutoField(primary_key=True)
    nama = models.CharField(max_length=100)  # Nama pegawai
    bidang = models.CharField(max_length=100)  # Nama bidang
    normalisasi_nilai = models.TextField()  # Normalisasi nilai dalam bentuk JSON string
    nilai_preferensi = models.FloatField()  # Nilai preferensi pegawai
    tahun_penilaian = models.IntegerField()  # Tahun penilaian (input dari user)

    def __str__(self):
        return f"{self.nama} - {self.nilai_preferensi:.2f} ({self.tahun_penilaian})"

    class Meta:
        verbose_name_plural = "Pegawai Terbaik"
        ordering = ['-tahun_penilaian', '-nilai_preferensi']
        
class RiwayatPenilaian(models.Model):
    id = models.AutoField(primary_key=True)  # ID otomatis
    nama = models.ForeignKey('Pegawai', on_delete=models.CASCADE)  # Relasi ke tabel Pegawai
    bidang = models.ForeignKey('Bidang', on_delete=models.CASCADE)  # Relasi ke tabel Bidang
    nilai = models.TextField()  # Nilai dalam format teks
    tahun_penilaian = models.IntegerField()
    
    def __str__(self):
        return f"Riwayat Penilaian {self.nama.nama} - {self.bidang.nama} ({self.tahun_penilaian})"
    
    class Meta:
        verbose_name_plural = "Riwayat Penilaian"
        ordering = ['id']

