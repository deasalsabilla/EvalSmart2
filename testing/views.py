from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Bidang, Pegawai, Kriteria, Penilaian, PegawaiTerbaik, RiwayatPenilaian
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
import json  # Untuk mengonversi data menjadi JSON
import ast  # Untuk parsing string dictionary

# mengarahkan ke halaman beranda
# Redirect ke halaman login jika belum login
@login_required(login_url='login')
def home(request):
    return render(request, 'index.html')

# fungsi login
def login(request):
    if request.method == "POST":
        # Ambil data dari form
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Autentikasi pengguna
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Login berhasil
            auth_login(request, user)
            return redirect('home')  # Ubah 'home' ke URL utama Anda
        else:
            # Login gagal
            messages.success(request, "Username atau password salah.")
            return redirect('login')

    # Jika request bukan POST, render halaman login
    return render(request, 'login.html')

# fungsi logout
def logout_view(request):
    logout(request)
    messages.success(request, "Anda telah berhasil logout.")
    return redirect('login')

# mengarahkan ke halaman kelola user
def user(request):
    # Ambil data user yang bukan staff dan aktif
    users = User.objects.filter(is_staff=False, is_active=True).order_by('id')
    return render(request, 'user.html', {'users': users})

# fungsi tambah user
def tambah_user(request):
    if request.method == "POST":
        # Ambil data dari form
        nama_depan = request.POST.get('nama_depan')
        nama_belakang = request.POST.get('nama_belakang')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        # Validasi input
        if password != password2:
            messages.error(
                request, "Password dan Konfirmasi Password tidak cocok.")
            return redirect('tambah_user')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username sudah digunakan.")
            return redirect('tambah_user')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email sudah terdaftar.")
            return redirect('tambah_user')

        # Simpan data user ke database
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=nama_depan,
            last_name=nama_belakang
        )
        user.save()
        messages.success(request, "User berhasil ditambahkan!")
        return redirect('user')  # Ubah sesuai kebutuhan

    # Jika request bukan POST, kembalikan halaman form
    return render(request, 'tambah_user.html')

# fungsi hapus user
def hapus_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        if not user.is_staff:  # Pastikan pengguna yang dihapus bukan staff
            user.delete()
            messages.success(request, "User berhasil dihapus.")
        else:
            messages.error(
                request, "Tidak dapat menghapus user dengan status staff.")
    except User.DoesNotExist:
        messages.error(request, "User tidak ditemukan.")
    return redirect('user')

# mengarahkan ke halaman kelola bidang dan menampilkan data bidang
def bidang(request):
    # Ambil semua data dari model Bidang
    bidangs = Bidang.objects.all()
    # Kirimkan data ke template
    return render(request, 'bidang.html', {'bidangs': bidangs})

# fungsi tambah bidang
def tambah_bidang(request):
    if request.method == "POST":
        # Ambil data dari input form
        nama_bidang = request.POST.get('nama_bidang')
        if nama_bidang:  # Validasi jika nama_bidang tidak kosong
            # Buat objek Bidang dan simpan ke database
            Bidang.objects.create(nama=nama_bidang)
            # Tambahkan pesan sukses
            messages.success(request, "Bidang berhasil ditambahkan!")
            # Redirect ke halaman daftar bidang
            return redirect('bidang')

        else:
            # Tambahkan pesan error jika input kosong
            messages.error(request, "Nama bidang tidak boleh kosong.")
            return redirect('tambah_bidang')

    # Render halaman tambah bidang
    return render(request, 'tambahBidang.html')

# Fungsi Edit Bidang
def edit_bidang(request, id):
    bidang = get_object_or_404(Bidang, id=id)
    if request.method == 'POST':
        bidang.nama = request.POST.get('nama', bidang.nama)
        bidang.save()
        messages.success(request, 'Bidang berhasil diubah!')
        return redirect('bidang')  # Kembali ke halaman tabel
    return render(request, 'edit_bidang.html', {'bidang': bidang})

# Fungsi Hapus Bidang
def delete_bidang(request, id):
    bidang = get_object_or_404(Bidang, id=id)
    if request.method == 'POST':
        bidang.delete()
        messages.success(request, 'Bidang berhasil dihapus!')
        return redirect('bidang')  # Kembali ke halaman tabel

# mengarahkan ke halaman dan menampilkan data kelola pegawai
def pegawai(request):
    pegawais = Pegawai.objects.all()
    return render(request, 'pegawai.html', {'pegawais' : pegawais})

# fungsi tambah pegawai
def tambah_pegawai(request):
    if request.method == "POST":
        nomor_induk = request.POST.get('nomor_induk')
        nama_pegawai = request.POST.get('nama_pegawai')
        alamat = request.POST.get('alamat')
        no_hp = request.POST.get('no_hp')
        bidang_id = request.POST.get('pilih_bidang')  # ID bidang dari dropdown

        # Validasi dan penyimpanan data
        try:
            bidang = Bidang.objects.get(id=bidang_id)  # Cari bidang berdasarkan ID
            # Simpan data ke model Pegawai
            pegawai = Pegawai.objects.create(
                nomor_induk=nomor_induk,
                nama=nama_pegawai,
                alamat=alamat,
                no_telp=no_hp,
                bidang=bidang
            )

            # Simpan data ke model Penilaian
            Penilaian.objects.create(
                nama=pegawai,
                bidang=bidang,
                nilai=None  # Biarkan nilai tetap kosong
            )

            messages.success(request, "Pegawai berhasil ditambahkan.")
            return redirect('pegawai')  # Redirect ke halaman tambah pegawai
        except Bidang.DoesNotExist:
            messages.error(request, "Bidang tidak ditemukan.")
        except Exception as e:
            messages.error(request, f"Terjadi kesalahan: {str(e)}")

    # Ambil data bidang untuk ditampilkan di dropdown
    bidang_list = Bidang.objects.all()
    return render(request, 'tambah_pegawai.html', {'bidang_list': bidang_list})

def edit_pegawai(request, pegawai_id):
    pegawai = get_object_or_404(Pegawai, id=pegawai_id)  # Ambil data pegawai berdasarkan ID
    bidang_list = Bidang.objects.all()  # Ambil semua bidang untuk dropdown

    if request.method == "POST":
        # Ambil data dari form
        nomor_induk = request.POST.get('nomor_induk')
        nama_pegawai = request.POST.get('nama_pegawai')
        alamat = request.POST.get('alamat')
        no_hp = request.POST.get('no_hp')
        bidang_id = request.POST.get('pilih_bidang')

        try:
            bidang_baru = Bidang.objects.get(id=bidang_id)

            # Cek perubahan nama dan bidang
            nama_lama = pegawai.nama
            bidang_lama = pegawai.bidang

            # Update data pegawai
            pegawai.nomor_induk = nomor_induk
            pegawai.nama = nama_pegawai
            pegawai.alamat = alamat
            pegawai.no_telp = no_hp
            pegawai.bidang = bidang_baru
            pegawai.save()  # Simpan perubahan ke database

            # Update model Penilaian jika nama atau bidang berubah
            if nama_pegawai != nama_lama or bidang_baru != bidang_lama:
                penilaian_terkait = Penilaian.objects.filter(nama=pegawai)
                for penilaian in penilaian_terkait:
                    penilaian.nama = pegawai  # Nama terkait otomatis berubah
                    penilaian.bidang = bidang_baru  # Bidang terkait diperbarui
                    penilaian.save()

            messages.success(request, "Data pegawai berhasil diperbarui.")
            return redirect('pegawai')  # Redirect ke halaman daftar pegawai (atau lainnya)
        except Bidang.DoesNotExist:
            messages.error(request, "Bidang tidak ditemukan.")
        except Exception as e:
            messages.error(request, f"Terjadi kesalahan: {str(e)}")

    return render(request, 'edit_pegawai.html', {'pegawai': pegawai, 'bidang_list': bidang_list})

# Fungsi Hapus Pegawai
def delete_pegawai(request, id):
    # Ambil data pegawai berdasarkan id
    pegawai = get_object_or_404(Pegawai, id=id)
    
    if request.method == 'POST':
        # Hapus semua data penilaian yang terkait dengan pegawai
        penilaian_terkait = Penilaian.objects.filter(nama=pegawai)  # Ubah 'pegawai' menjadi 'nama'
        penilaian_terkait.delete()
        
        # Hapus data pegawai
        pegawai.delete()
        
        # Kirim pesan sukses
        messages.success(request, 'Pegawai berhasil dihapus!')
        
        # Redirect ke halaman tabel pegawai
        return redirect('pegawai')

# mengarahkan ke halaman kelola kriteria
def kriteria(request):
    kriterias = Kriteria.objects.all()
    return render(request, 'kriteria.html', {'kriterias' : kriterias})

# fungsi tambah kriteria
def tambah_kriteria(request):
    if request.method == "POST":
        # Ambil data dari input form
        nama_kriteria = request.POST.get('nama_kriteria')
        tipe_kriteria = request.POST.get('tipe_kriteria')  # Ambil tipe kriteria dari form

        if nama_kriteria and tipe_kriteria:  # Validasi jika nama_kriteria dan tipe_kriteria tidak kosong
            # Buat objek Kriteria dan simpan ke database
            kriteria = Kriteria.objects.create(nama=nama_kriteria, tipe=tipe_kriteria)
            
            # Update kolom nilai di semua Penilaian
            penilaian_list = Penilaian.objects.all()
            for penilaian in penilaian_list:
                if penilaian.nilai:  # Cek jika kolom nilai tidak kosong
                    # Load nilai dari JSON
                    nilai_dict = json.loads(penilaian.nilai)
                    # Tambahkan kriteria baru dengan nilai default 0
                    nilai_dict[kriteria.nama] = 0
                    # Simpan kembali ke database
                    penilaian.nilai = json.dumps(nilai_dict)
                    penilaian.save()

            # Tambahkan pesan sukses
            messages.success(request, "Kriteria berhasil ditambahkan!")
            # Redirect ke halaman daftar kriteria
            return redirect('kriteria')

        else:
            # Tambahkan pesan error jika input kosong
            messages.error(request, "Nama kriteria dan tipe kriteria tidak boleh kosong.")
            return redirect('tambah_kriteria')

    return render(request, 'tambah_kriteria.html')

# Fungsi Edit Kriteria
def edit_kriteria(request, id):
    kriteria = get_object_or_404(Kriteria, id=id)
    if request.method == 'POST':
        # Ambil data dari form
        nama_kriteria_baru = request.POST.get('nama', kriteria.nama)
        tipe_kriteria = request.POST.get('tipe', kriteria.tipe)

        # Validasi tipe kriteria
        if tipe_kriteria not in ['benefit', 'cost']:
            messages.error(request, "Tipe kriteria tidak valid.")
            return redirect('edit_kriteria', id=id)

        # Jika nama kriteria diubah, update kolom nilai pada Penilaian
        if nama_kriteria_baru != kriteria.nama:
            penilaian_list = Penilaian.objects.all()
            for penilaian in penilaian_list:
                if penilaian.nilai:  # Pastikan kolom nilai tidak kosong
                    nilai_dict = json.loads(penilaian.nilai)  # Parse JSON ke dictionary
                    if kriteria.nama in nilai_dict:  # Cek apakah kriteria ada di nilai
                        nilai_dict[nama_kriteria_baru] = nilai_dict.pop(kriteria.nama)  # Ganti nama kriteria
                        penilaian.nilai = json.dumps(nilai_dict)  # Simpan kembali dalam format JSON
                        penilaian.save()

        # Simpan perubahan pada model Kriteria
        kriteria.nama = nama_kriteria_baru
        kriteria.tipe = tipe_kriteria
        kriteria.save()
        
        messages.success(request, 'Kriteria berhasil diubah!')
        return redirect('kriteria')  # Kembali ke halaman tabel

    # Data untuk template
    return render(request, 'edit_kriteria.html', {'kriteria': kriteria})

# Fungsi Hapus Kriteria
def delete_kriteria(request, id):
    kriteria = get_object_or_404(Kriteria, id=id)
    if request.method == 'POST':
        penilaian_list = Penilaian.objects.all()

        # Hapus kriteria dari kolom nilai pada setiap Penilaian
        for penilaian in penilaian_list:
            if penilaian.nilai:  # Pastikan kolom nilai tidak kosong
                nilai_dict = json.loads(penilaian.nilai)  # Parse JSON ke dictionary
                if kriteria.nama in nilai_dict:  # Cek apakah kriteria ada di nilai
                    del nilai_dict[kriteria.nama]  # Hapus kriteria dari dictionary
                    penilaian.nilai = json.dumps(nilai_dict)  # Simpan kembali dalam format JSON
                    penilaian.save()

        # Hapus kriteria dari database
        kriteria.delete()
        messages.success(request, 'Kriteria berhasil dihapus!')
        return redirect('kriteria')  # Kembali ke halaman tabel

    # Data untuk konfirmasi penghapusan
    return render(request, 'delete_kriteria.html', {'kriteria': kriteria})

    
# fungsi input bobot
def input_bobot(request, kriteria_id):
    # Ambil kriteria berdasarkan ID
    kriteria = get_object_or_404(Kriteria, id=kriteria_id)

    if request.method == "POST":
        try:
            bobot_baru = float(request.POST.get('bobot', 0))  # Ambil bobot baru dari form
            total_bobot_sekarang = Kriteria.objects.exclude(id=kriteria.id).aggregate(total=Sum('bobot'))['total'] or 0

            # Hitung total bobot jika bobot baru ditambahkan
            total_bobot_setelah_input = total_bobot_sekarang + bobot_baru

            if total_bobot_setelah_input > 100:
                # Jika total bobot melebihi 100, tampilkan pesan error
                messages.error(
                    request, 
                    f"Bobot yang Anda masukkan melebihi batas. Maksimal yang bisa ditambahkan adalah {100 - total_bobot_sekarang:.2f}%."
                )
            else:
                # Simpan bobot baru ke kriteria yang sudah ada
                kriteria.bobot = bobot_baru
                kriteria.save()

                messages.success(request, f"Bobot untuk {kriteria.nama} berhasil diperbarui.")
                return redirect('kriteria')  # Ganti dengan URL yang sesuai
        except ValueError:
            messages.error(request, "Bobot harus berupa angka yang valid.")
    
    # Data untuk ditampilkan di template
    total_bobot_sekarang = Kriteria.objects.exclude(id=kriteria.id).aggregate(total=Sum('bobot'))['total'] or 0
    context = {
        'kriteria': kriteria,
        'total_bobot_sekarang': total_bobot_sekarang,
        'bobot_maksimal': 100 - total_bobot_sekarang,
    }
    return render(request, 'bobot_kriteria.html', context)

# mengarahkan ke halaman kelola penilaian
def penilaian(request):
    if request.GET.get("success") == "true":
        messages.success(request, "Pemilihan pegawai terbaik sudah selesai. Jika ingin melihat kembali Penilaian dan Pegawai terbaik dapat melihat pada menu Riwayat.")
    # Ambil semua data dari model Penilaian
    penilaian_list = Penilaian.objects.all()
    return render(request, 'penilaian.html', {'penilaian_list': penilaian_list})

def input_nilai(request, id):
    penilaian = get_object_or_404(Penilaian, id=id)  # Ambil data Penilaian berdasarkan ID
    kriteria_list = Kriteria.objects.all()          # Ambil semua kriteria
    
    if request.method == 'POST':
        # Ambil nilai dari form input
        nilai_dict = {}
        for kriteria in kriteria_list:
            nilai = request.POST.get(kriteria.nama)
            if nilai:
                nilai_dict[kriteria.nama] = int(nilai)  # Pastikan nilai berupa integer
        
        # Simpan data ke kolom nilai dalam format JSON
        penilaian.nilai = json.dumps(nilai_dict)
        penilaian.save()

        messages.success(request, 'Nilai Berhasil ditambahkan!')
        # Redirect setelah berhasil menyimpan
        return redirect('penilaian')  # Ganti dengan nama URL untuk halaman daftar penilaian

    context = {
        'penilaian': penilaian,
        'kriteria_list': kriteria_list,
    }
    return render(request, 'input_nilai.html', context)

def lihat_nilai(request, penilaian_id):
    # Ambil data penilaian berdasarkan ID
    penilaian = get_object_or_404(Penilaian, id=penilaian_id)

    # Parsing kolom nilai dari string ke dictionary
    try:
        nilai_dict = ast.literal_eval(penilaian.nilai) if penilaian.nilai else {}
    except Exception:
        nilai_dict = {}

    context = {
        'penilaian': penilaian,
        'nilai_dict': nilai_dict,
    }
    return render(request, 'lihat_nilai.html', context)

def edit_nilai(request, id):
    # Ambil data penilaian berdasarkan ID
    penilaian = get_object_or_404(Penilaian, id=id)

    # Ambil daftar kriteria
    kriteria_list = Kriteria.objects.all()

    # Muat nilai dari kolom nilai (format JSON) jika tidak kosong
    nilai_dict = json.loads(penilaian.nilai) if penilaian.nilai else {}

    # Buat pasangan (kriteria, nilai) untuk akses lebih mudah di template
    nilai_data = [(kriteria.nama, nilai_dict.get(kriteria.nama, '')) for kriteria in kriteria_list]

    if request.method == "POST":
        try:
            # Perbarui nilai berdasarkan input dari form
            for kriteria in kriteria_list:
                nilai_input = request.POST.get(kriteria.nama)
                if nilai_input:
                    nilai_dict[kriteria.nama] = int(nilai_input)  # Simpan nilai sebagai integer
            
            # Simpan kembali nilai ke database
            penilaian.nilai = json.dumps(nilai_dict)
            penilaian.save()

            messages.success(request, "Nilai berhasil diperbarui!")
            return redirect('lihat_nilai', penilaian.id)

        except Exception as e:
            messages.error(request, f"Terjadi kesalahan: {str(e)}")

    context = {
        'penilaian': penilaian,
        'nilai_data': nilai_data,  # Data (kriteria, nilai)
    }
    return render(request, 'edit_nilai.html', context)

def hitung_normalisasi_saw(nilai, tipe, max_nilai, min_nilai):
    """Fungsi untuk menghitung normalisasi nilai berdasarkan metode SAW."""
    if tipe == 'benefit':
        return nilai / max_nilai if max_nilai > 0 else 0
    elif tipe == 'cost':
        return min_nilai / nilai if nilai > 0 else 0
    return 0

def pegawai_terbaik(request):
    if request.method == "POST":
        tahun_penilaian = request.POST.get("tahun_nilai")

        # Validasi total bobot kriteria
        kriteria = Kriteria.objects.all()
        total_bobot = sum([k.bobot for k in kriteria])
        if total_bobot != 100:
            messages.error(request, "Total bobot kriteria harus 100%. Harap perbaiki bobot kriteria.")
            return redirect("kriteria")

        # Validasi apakah semua nilai di Penilaian sesuai dengan tahun_penilaian
        penilaian = Penilaian.objects.all()
        riwayat_penilaian_tahun_ini = RiwayatPenilaian.objects.filter(tahun_penilaian=tahun_penilaian)

        if riwayat_penilaian_tahun_ini.exists():
            messages.error(request, f"Pemilihan pegawai terbaik untuk tahun {tahun_penilaian} sudah ada.")
            return redirect("penilaian")

        for p in penilaian:
            nilai_dict = json.loads(p.nilai) if p.nilai else {}
            if not nilai_dict or not all(isinstance(val, (int, float)) for val in nilai_dict.values()):
                messages.error(request, f"Nilai untuk pegawai {p.nama.nama} belum lengkap atau tidak valid. Harap isi nilai dengan benar untuk tahun {tahun_penilaian}.")
                return redirect("penilaian")

        # Simpan semua data penilaian ke dalam model RiwayatPenilaian
        for p in penilaian:
            RiwayatPenilaian.objects.create(
                nama=p.nama,
                bidang=p.bidang,
                nilai=p.nilai,
                tahun_penilaian=tahun_penilaian,
            )

        # Hitung min dan max nilai untuk setiap kriteria berdasarkan tipe
        min_max_per_kriteria = {}
        for k in kriteria:
            nilai_kriteria = []
            for p in penilaian:
                nilai_dict = json.loads(p.nilai)
                if k.nama in nilai_dict:
                    nilai_kriteria.append(nilai_dict[k.nama])
            min_max_per_kriteria[k.nama] = {
                'min': min(nilai_kriteria) if nilai_kriteria else 0,
                'max': max(nilai_kriteria) if nilai_kriteria else 0,
            }

        # Proses perhitungan normalisasi dan preferensi
        PegawaiTerbaik.objects.filter(tahun_penilaian=tahun_penilaian).delete()
        for p in penilaian:
            nilai_dict = json.loads(p.nilai)
            normalisasi = {}
            nilai_preferensi = 0

            for k in kriteria:
                nilai = nilai_dict.get(k.nama, 0)
                max_nilai = min_max_per_kriteria[k.nama]['max']
                min_nilai = min_max_per_kriteria[k.nama]['min']

                if k.tipe == 'benefit' and max_nilai > 0:
                    normalisasi_nilai = nilai / max_nilai
                elif k.tipe == 'cost' and nilai > 0:
                    normalisasi_nilai = min_nilai / nilai
                else:
                    normalisasi_nilai = 0

                normalisasi[k.nama] = normalisasi_nilai
                nilai_preferensi += normalisasi_nilai * (k.bobot / 100)

            PegawaiTerbaik.objects.create(
                nama=p.nama.nama,
                bidang=p.bidang.nama,
                normalisasi_nilai=json.dumps(normalisasi),
                nilai_preferensi=nilai_preferensi,
                tahun_penilaian=tahun_penilaian,
            )
            
        # Reset kolom nilai pada model Penilaian setelah berhasil menyimpan data
        Penilaian.objects.update(nilai=None)

        # Ambil 10 pegawai terbaik berdasarkan nilai preferensi
        pegawai_terbaik = PegawaiTerbaik.objects.filter(
            tahun_penilaian=tahun_penilaian
        ).order_by('-nilai_preferensi')[:10]

        return render(request, 'pegawai_terbaik.html', {
            'pegawai_terbaik': pegawai_terbaik,
        })

    return render(request, 'pegawai_terbaik.html')

# mengarahkan ke halaman riwayat
def riwayat(request):
    # Mengambil daftar tahun unik dari PegawaiTerbaik
    tahun_list = PegawaiTerbaik.objects.values_list('tahun_penilaian', flat=True).distinct().order_by('tahun_penilaian')

    # Menangkap pilihan select
    riwayat_type = request.GET.get('riwayat_type')  # Jenis riwayat
    tahun = request.GET.get('tahun')  # Tahun yang dipilih

    # Data default kosong
    data_riwayat = []
    if riwayat_type == "pegawai_terbaik" and tahun:
        # Filter PegawaiTerbaik berdasarkan tahun
        data_riwayat = PegawaiTerbaik.objects.filter(tahun_penilaian=tahun)
    elif riwayat_type == "riwayat_penilaian" and tahun:
        # Filter RiwayatPenilaian berdasarkan tahun
        data_riwayat = RiwayatPenilaian.objects.filter(tahun_penilaian=tahun)

    return render(request, 'riwayat.html', {
        'tahun_list': tahun_list,
        'data_riwayat': data_riwayat,
        'riwayat_type': riwayat_type,
        'tahun': tahun,
    })