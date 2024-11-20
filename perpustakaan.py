import streamlit as st
import qrcode
import pandas as pd
from PIL import Image
from io import BytesIO
import json

# Fungsi untuk membuat QR code
def buat_qr_code(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

# Fungsi untuk membaca data dari file JSON
def baca_data_dari_file(nama_file):
    try:
        with open(nama_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        st.error(f"File '{nama_file}' tidak ditemukan.")
    except json.JSONDecodeError:
        st.error(f"Format file '{nama_file}' tidak valid.")
    return None

# Fungsi untuk mencari laporan PKL berdasarkan judul
def cari_laporan(judul_dicari, data):
    for laporan in data:
        if 'judul_laporan_pkl' in laporan and laporan['judul_laporan_pkl'].lower() == judul_dicari.lower():
            return laporan
    return None

# Set konfigurasi halaman Streamlit
st.set_page_config(page_title="Pencarian Laporan PKL", layout="wide")

# Tampilkan QR code untuk aplikasi di perangkat mobile
url_aplikasi = "https://pencarian-laporan-pkl.streamlit.app/"  # Ganti dengan URL aplikasi Anda
qr_code = buat_qr_code(url_aplikasi)
qr_image = Image.open(qr_code)

# Sidebar
st.sidebar.image(qr_image, caption="Scan QR untuk Akses Aplikasi di HP")
st.sidebar.header("Pencarian Laporan PKL")
st.sidebar.markdown("Gunakan aplikasi ini untuk mencari laporan PKL berdasarkan judul.")

# Nama file JSON
nama_file = 'datajsonpkl.json'

# Membaca data dari file JSON
data_perpustakaan = baca_data_dari_file(nama_file)

# Jika data berhasil dibaca
if data_perpustakaan:
    # Ambil daftar judul laporan PKL dari data
    daftar_judul = ["Pilih Judul Laporan PKL"] + [
        laporan.get('judul_laporan_pkl', 'Judul Tidak Tersedia') for laporan in data_perpustakaan
    ]

    # Input pengguna
    judul_yang_dicari = st.selectbox("Pilih Judul Laporan PKL:", daftar_judul)

    # Tombol untuk mencari
    if st.button("Cari"):
        if judul_yang_dicari != "Pilih Judul Laporan PKL":
            # Cari laporan PKL berdasarkan judul
            laporan_ditemukan = cari_laporan(judul_yang_dicari, data_perpustakaan)

            # Menampilkan hasil
            if laporan_ditemukan:
                df = pd.DataFrame([laporan_ditemukan])
                df['No'] = range(1, len(df) + 1)
                df = df.rename(columns={
                    'nomor_urut': 'Nomor Urut',
                    'arsip_laporan_pkl': 'Arsip Laporan PKL',
                    'tahun_pelaksanaan': 'Tahun Pelaksanaan',
                    'nim': 'NIM',
                    'nama_mahasiswa': 'Nama Mahasiswa',
                    'judul_laporan_pkl': 'Judul Laporan PKL',
                    'nama_dosen_pembimbing': 'Nama Dosen Pembimbing',
                    'nama_tempat_pelaksanaan': 'Nama Tempat Pelaksanaan',
                    'kabupaten_kota': 'Kabupaten/Kota'
                })
                df = df[['Nomor Urut', 'Arsip Laporan PKL', 'Tahun Pelaksanaan', 'NIM',
                         'Nama Mahasiswa', 'Judul Laporan PKL', 'Nama Dosen Pembimbing',
                         'Nama Tempat Pelaksanaan', 'Kabupaten/Kota']]
                st.subheader(f"Detail Laporan PKL '{judul_yang_dicari}':")
                st.write(df.to_html(index=False), unsafe_allow_html=True)
            else:
                st.warning("Laporan PKL tidak ditemukan.")
        else:
            st.warning("Silakan pilih judul laporan PKL.")
else:
    st.error("Data laporan PKL tidak tersedia.")
