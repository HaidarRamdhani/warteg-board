import streamlit as st
import base64
import json
from datetime import date
# ==============================================================================
# BLOK CSS FINAL v3 (MENJAMIN ADA JARAK DALAM BOX)
# ==============================================================================
st.markdown("""
<style>
    /* 1. PAKSA AREA KONTEN EXPANDER UNTUK PUNYA PADDING (Batas Dalam) */
    div[data-testid="stExpanderDetails"] {
        padding: 0.5rem 2.5rem 1rem 2rem !important; /* top | right | bottom | left */
    }

    /* 2. Atur baris (st.columns) di dalam expander agar sejajar & tidak turun baris */
    div[data-testid="stExpander"] div[data-testid="stHorizontalBlock"] {
        display: flex;
        align-items: center;
        flex-wrap: nowrap;
        gap: 0.5rem; /* Jarak antara checkbox dan tombol */
    }

    /* 3. Atur kolom checkbox (kolom pertama) agar bisa memanjang */
    div[data-testid="stExpander"] div[data-testid="stHorizontalBlock"] > div:first-child {
        overflow: hidden;
        flex-grow: 1;
    }

    /* 4. Atur kolom tombol (kolom terakhir) agar ukurannya pas */
    div[data-testid="stExpander"] div[data-testid="stHorizontalBlock"] > div:last-child {
        flex-grow: 0;
    }

    /* 5. Atur tombolnya agar kecil dan rapi */
    div[data-testid="stExpander"] div[data-testid="stHorizontalBlock"] button {
        padding: 0.2rem 0.5rem;
        margin: 0;
        line-height: 1;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# FUNGSI-FUNGSI PEMBANTU
# ==============================================================================

@st.cache_data
def get_image_as_base64(path: str) -> str | None:
    """
    Membaca file gambar dari path yang diberikan dan mengubahnya menjadi 
    string Base64. Menggunakan cache agar proses ini hanya berjalan sekali 
    per gambar, sehingga aplikasi tetap cepat.
    """
    try:
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        # Jika file tidak ditemukan, tampilkan peringatan di konsol
        # dan kembalikan None agar bisa ditangani di UI.
        print(f"Peringatan: File gambar tidak ditemukan di path: {path}")
        return None

# --- FUNGSI BARU UNTUK LAYOUT 2 KOLOM ---
def tampilkan_petugas(daftar_petugas: list[dict]):
    """
    Menampilkan daftar petugas dalam layout DUA KOLOM,
    ideal untuk tampilan mobile.
    """
    # Buat dua kolom utama untuk menampung daftar
    kolom_kiri, kolom_kanan = st.columns(2)

    # Iterasi pada daftar petugas dengan langkah 2
    for i in range(0, len(daftar_petugas), 2):
        # Proses petugas di kolom kiri
        orang_kiri = daftar_petugas[i]
        with kolom_kiri:
            # Panggil fungsi untuk render satu item
            render_satu_petugas(orang_kiri)

        # Cek apakah ada pasangan untuk kolom kanan
        if i + 1 < len(daftar_petugas):
            orang_kanan = daftar_petugas[i+1]
            with kolom_kanan:
                # Panggil fungsi untuk render satu item
                render_satu_petugas(orang_kanan)

def render_satu_petugas(orang: dict):
    """
    Fungsi ini bertanggung jawab untuk me-render SATU item petugas
    (gambar dan nama). Dipanggil oleh tampilkan_petugas.
    """
    base64_image = get_image_as_base64(orang["gambar"])
    
    if base64_image:
        # Menggunakan HTML untuk layout yang lebih ringkas dan terpusat
        item_html = f"""
            <div style="display: flex; flex-direction: column; align-items: center; margin-bottom: 20px;">
                <img src="data:image/png;base64,{base64_image}"
                     style="
                        width: 120px;
                        height: 120px;
                        object-fit: cover;
                        border-radius: 50%; /* Membuat gambar menjadi bulat */
                        margin-bottom: 8px;
                        image-rendering: -webkit-optimize-contrast;
                        image-rendering: crisp-edges;
                     "
                >
                <div style="font-weight: bold; text-align: center;">{orang['nama']}</div>
            </div>
        """
        st.markdown(item_html, unsafe_allow_html=True)
    else:
        # Placeholder jika gambar tidak ditemukan
        st.markdown(
            f"""
            <div style="display: flex; flex-direction: column; align-items: center; margin-bottom: 20px;">
                <div style="width:80px; height:80px; background-color:#ddd; border-radius:50%;"></div>
                <div style="font-weight: bold; text-align: center; margin-top: 8px;">{orang['nama']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ==============================================================================
# KONFIGURASI DAN DATA
# ==============================================================================

# Konfigurasi halaman utama
st.set_page_config(page_title="Dashboard WarTeg", layout="wide")

# Data jadwal. Pastikan path 'assets/NamaFile.png' sudah benar.
# Sebaiknya gunakan file thumbnail berukuran 128x128px untuk hasil terbaik.
jadwal = {
    "2025-07-01": {
        "hari": "Selasa",
        "balai_desa": [
            {"nama": "Via", "gambar": "assets/Via.png"},
            {"nama": "Deni", "gambar": "assets/Deni.png"}
        ],
        "masak": [
            {"nama": "Atika", "gambar": "assets/Atika.png"},
            {"nama": "Riska", "gambar": "assets/Riska.png"},
            {"nama": "Iqbal", "gambar": "assets/Iqbal.png"},
            {"nama": "Gina", "gambar": "assets/Gina.png"}
        ],
        "lain_lain": None
    },
    "2025-07-02": {
        "hari": "Rabu",
        "balai_desa": [
            {"nama": "Riska", "gambar": "assets/Riska.png"},
            {"nama": "Atika", "gambar": "assets/Atika.png"}
        ],
        "masak": [
            {"nama": "Haidar", "gambar": "assets/Haidar.png"},
            {"nama": "Gina", "gambar": "assets/Gina.png"},
            {"nama": "Via", "gambar": "assets/Via.png"},
            {"nama": "Lomi", "gambar": "assets/Lomi.png"}
        ],
        "lain_lain": None
    },
    "2025-07-03": {
        "hari": "Kamis",
        "balai_desa": [
            {"nama": "Gina", "gambar": "assets/Gina.png"},
            {"nama": "Lomi", "gambar": "assets/Lomi.png"}
        ],
        "masak": [
            {"nama": "Iqbal", "gambar": "assets/Iqbal.png"},
            {"nama": "Deni", "gambar": "assets/Deni.png"},
            {"nama": "Atika", "gambar": "assets/Atika.png"},
            {"nama": "Riska", "gambar": "assets/Riska.png"}
        ],
        "lain_lain": None
    },
    "2025-07-04": {
        "hari": "Jumat",
        "balai_desa": None,
        "masak": [
            {"nama": "Haidar", "gambar": "assets/Haidar.png"},
            {"nama": "Gina", "gambar": "assets/Gina.png"},
            {"nama": "Via", "gambar": "assets/Via.png"},
            {"nama": "Lomi", "gambar": "assets/Lomi.png"}
        ],
        "lain_lain": None
    },
    "2025-07-05": {
        "hari": "Sabtu",
        "balai_desa": None,
        "masak": None,
        "lain_lain": None
    },
    "2025-07-06": {
        "hari": "Minggu",
        "balai_desa": None,
        "masak": None,
        "lain_lain": None
    },
     "2025-07-07": {
        "hari": "Senin",
        "balai_desa": [
            {"nama": "Gina", "gambar": "assets/Gina.png"},
            {"nama": "Atika", "gambar": "assets/Atika.png"}
        ],
        "masak": [
            {"nama": "Iqbal", "gambar": "assets/Iqbal.png"},
            {"nama": "Deni", "gambar": "assets/Deni.png"},
            {"nama": "Via", "gambar": "assets/Via.png"},
            {"nama": "Riska", "gambar": "assets/Riska.png"}
        ],
        "lain_lain": None
    },
     "2025-07-08": {
        "hari": "Selasa",
        "balai_desa": [
            {"nama": "Iqbal", "gambar": "assets/Iqbal.png"},
            {"nama": "Deni", "gambar": "assets/Deni.png"}
        ],
        "masak": [
            {"nama": "Haidar", "gambar": "assets/Haidar.png"},
            {"nama": "Lomi", "gambar": "assets/Lomi.png"},
            {"nama": "Atika", "gambar": "assets/Atika.png"},
            {"nama": "Gina", "gambar": "assets/Gina.png"}
        ],
        "lain_lain": None
    },
    "2025-07-09": {
        "hari": "Rabu",
        "balai_desa": [
            {"nama": "Haidar", "gambar": "assets/Haidar.png"},
            {"nama": "Lomi", "gambar": "assets/Lomi.png"}
        ],
        "masak": [
            {"nama": "Iqbal", "gambar": "assets/Iqbal.png"},
            {"nama": "Deni", "gambar": "assets/Deni.png"},
            {"nama": "Via", "gambar": "assets/Via.png"},
            {"nama": "Riska", "gambar": "assets/Riska.png"}
        ],
        "lain_lain": None
    },
    "2025-07-10": {
        "hari": "Kamis",
        "balai_desa": [
            {"nama": "Riska", "gambar": "assets/Riska.png"},
            {"nama": "Via", "gambar": "assets/Via.png"}
        ],
        "masak": [
            {"nama": "Haidar", "gambar": "assets/Haidar.png"},
            {"nama": "Lomi", "gambar": "assets/Lomi.png"},
            {"nama": "Atika", "gambar": "assets/Atika.png"},
            {"nama": "Gina", "gambar": "assets/Gina.png"}
        ],
        "lain_lain": None
    },
    "2025-07-11": {
        "hari": "Jumat",
        "balai_desa": None,
        "masak": [
            {"nama": "Iqbal", "gambar": "assets/Iqbal.png"},
            {"nama": "Deni", "gambar": "assets/Deni.png"},
            {"nama": "Via", "gambar": "assets/Via.png"},
            {"nama": "Riska", "gambar": "assets/Riska.png"}
        ],
        "lain_lain": None
    },
    "2025-07-12": {
        "hari": "Sabtu",
        "balai_desa": None,
        "masak": None,
        "lain_lain": None
    },
    "2025-07-13": {
        "hari": "Minggu",
        "balai_desa": None,
        "masak": None,
        "lain_lain": None
    },
    "2025-07-14": {
        "hari": "Senin",
        "balai_desa": [
            {"nama": "Riska", "gambar": "assets/Riska.png"},
            {"nama": "Lomi", "gambar": "assets/Lomi.png"}
        ],
        "masak": [
            {"nama": "Haidar", "gambar": "assets/Haidar.png"},
            {"nama": "Deni", "gambar": "assets/Deni.png"},
            {"nama": "Atika", "gambar": "assets/Atika.png"},
            {"nama": "Via", "gambar": "assets/Via.png"}
        ],
        "lain_lain": None
    },
    "2025-07-15": {
        "hari": "Selasa",
        "balai_desa": [
            {"nama": "Atika", "gambar": "assets/Atika.png"},
            {"nama": "Haidar", "gambar": "assets/Haidar.png"}
        ],
        "masak": [
            {"nama": "Iqbal", "gambar": "assets/Iqbal.png"},
            {"nama": "Riska", "gambar": "assets/Riska.png"},
            {"nama": "Lomi", "gambar": "assets/Lomi.png"},
            {"nama": "Gina", "gambar": "assets/Gina.png"}
        ],
        "lain_lain": None
    },
    "2025-07-16": {
        "hari": "Rabu",
        "balai_desa": [
            {"nama": "Gina", "gambar": "assets/Gina.png"},
            {"nama": "Iqbal", "gambar": "assets/Iqbal.png"}
        ],
        "masak": [
            {"nama": "Haidar", "gambar": "assets/Haidar.png"},
            {"nama": "Deni", "gambar": "assets/Deni.png"},
            {"nama": "Atika", "gambar": "assets/Atika.png"},
            {"nama": "Via", "gambar": "assets/Via.png"}
        ],
        "lain_lain": None
    },
    "2025-07-17": {
        "hari": "Kamis",
        "balai_desa": [
            {"nama": "Via", "gambar": "assets/Via.png"},
            {"nama": "Deni", "gambar": "assets/Deni.png"}
        ],
        "masak": [
            {"nama": "Iqbal", "gambar": "assets/Iqbal.png"},
            {"nama": "Riska", "gambar": "assets/Riska.png"},
            {"nama": "Lomi", "gambar": "assets/Lomi.png"},
            {"nama": "Gina", "gambar": "assets/Gina.png"}
        ],
        "lain_lain": None
    },
    "2025-07-18": {
        "hari": "Jumat",
        "balai_desa": None,
        "masak": [
            {"nama": "Haidar", "gambar": "assets/Haidar.png"},
            {"nama": "Deni", "gambar": "assets/Deni.png"},
            {"nama": "Atika", "gambar": "assets/Atika.png"},
            {"nama": "Via", "gambar": "assets/Via.png"}
        ],
        "lain_lain": None
    },
    "2025-07-19": {
        "hari": "Sabtu",
        "balai_desa": None,
        "masak": None,
        "lain_lain": None
    },
    "2025-07-20": {
        "hari": "Minggu",
        "balai_desa": None,
        "masak": None,
        "lain_lain": None
    },
    "2025-07-21": {
        "hari": "Senin",
        "balai_desa": [
            {"nama": "Via", "gambar": "assets/Via.png"},
            {"nama": "Haidar", "gambar": "assets/Haidar.png"}
        ],
        "masak": [
            {"nama": "Iqbal", "gambar": "assets/Iqbal.png"},
            {"nama": "Deni", "gambar": "assets/Deni.png"},
            {"nama": "Lomi", "gambar": "assets/Lomi.png"},
            {"nama": "Atika", "gambar": "assets/Atika.png"}
        ],
        "lain_lain": None
    },
    "2025-07-22": {
        "hari": "Selasa",
        "balai_desa": [
            {"nama": "Atika", "gambar": "assets/Atika.png"},
            {"nama": "Deni", "gambar": "assets/Deni.png"}
        ],
        "masak": [
            {"nama": "Via", "gambar": "assets/Via.png"},
            {"nama": "Riska", "gambar": "assets/Riska.png"},
            {"nama": "Haidar", "gambar": "assets/Haidar.png"},
            {"nama": "Gina", "gambar": "assets/Gina.png"}
        ],
        "lain_lain": None
    },
    "2025-07-23": {
        "hari": "Rabu",
        "balai_desa": [
            {"nama": "Gina", "gambar": "assets/Gina.png"},
            {"nama": "Riska", "gambar": "assets/Riska.png"}
        ],
        "masak": [
            {"nama": "Iqbal", "gambar": "assets/Iqbal.png"},
            {"nama": "Deni", "gambar": "assets/Deni.png"},
            {"nama": "Lomi", "gambar": "assets/Lomi.png"},
            {"nama": "Atika", "gambar": "assets/Atika.png"}
        ],
        "lain_lain": None
    },
    "2025-07-24": {
        "hari": "Kamis",
        "balai_desa": [
            {"nama": "Iqbal", "gambar": "assets/Iqbal.png"},
            {"nama": "Lomi", "gambar": "assets/Lomi.png"}
        ],
        "masak": [
            {"nama": "Via", "gambar": "assets/Via.png"},
            {"nama": "Riska", "gambar": "assets/Riska.png"},
            {"nama": "Haidar", "gambar": "assets/Haidar.png"},
            {"nama": "Gina", "gambar": "assets/Gina.png"}
        ],
        "lain_lain": None
    },
    "2025-07-25": {
        "hari": "Jumat",
        "balai_desa": None,
        "masak": [
            {"nama": "Iqbal", "gambar": "assets/Iqbal.png"},
            {"nama": "Deni", "gambar": "assets/Deni.png"},
            {"nama": "Lomi", "gambar": "assets/Lomi.png"},
            {"nama": "Atika", "gambar": "assets/Atika.png"}
        ],
        "lain_lain": None
    },
    "2025-07-26": {
        "hari": "Sabtu",
        "balai_desa": None,
        "masak": None,
        "lain_lain": None
    },
    "2025-07-27": {
        "hari": "Minggu",
        "balai_desa": None,
        "masak": None,
        "lain_lain": None
    },
    "2025-07-28": {
        "hari": "Senin",
        "balai_desa": [
            {"nama": "Atika", "gambar": "assets/Atika.png"},
            {"nama": "Gina", "gambar": "assets/Gina.png"}
        ],
        "masak": [
            {"nama": "Via", "gambar": "assets/Via.png"},
            {"nama": "Lomi", "gambar": "assets/Lomi.png"},
            {"nama": "Haidar", "gambar": "assets/Haidar.png"},
            {"nama": "Iqbal", "gambar": "assets/Iqbal.png"}
        ],
        "lain_lain": None
    },
    "2025-07-29": {
        "hari": "Selasa",
        "balai_desa": [
            {"nama": "Lomi", "gambar": "assets/Lomi.png"},
            {"nama": "Via", "gambar": "assets/Via.png"}
        ],
        "masak": [
            {"nama": "Atika", "gambar": "assets/Gina.png"},
            {"nama": "Deni", "gambar": "assets/Deni.png"},
            {"nama": "Riska", "gambar": "assets/Riska.png"},
            {"nama": "Gina", "gambar": "assets/Gina.png"}
        ],
        "lain_lain": None
    },
    "2025-07-30": {
        "hari": "Rabu",
        "balai_desa": [
            {"nama": "Deni", "gambar": "assets/Deni.png"},
            {"nama": "Haidar", "gambar": "assets/Haidar.png"}
        ],
        "masak": [
            {"nama": "Via", "gambar": "assets/Via.png"},
            {"nama": "Lomi", "gambar": "assets/Lomi.png"},
            {"nama": "Gina", "gambar": "assets/Gina.png"},
            {"nama": "Iqbal", "gambar": "assets/Iqbal.png"}
        ],
        "lain_lain": None
    },
    "2025-07-31": {
        "hari": "Kamis",
        "balai_desa": [
            {"nama": "Iqbal", "gambar": "assets/Iqbal.png"},
            {"nama": "Riska", "gambar": "assets/Riska.png"}
        ],
        "masak": [
            {"nama": "Via", "gambar": "assets/Via.png"},
            {"nama": "Lomi", "gambar": "assets/Lomi.png"},
            {"nama": "Haidar", "gambar": "assets/Haidar.png"},
            {"nama": "Atika", "gambar": "assets/Atika.png"}
        ],
        "lain_lain": None
    },
    "2025-08-01": {
        "hari": "Jumat",
        "balai_desa": None,
        "masak": [
            {"nama": "Via", "gambar": "assets/Via.png"},
            {"nama": "Lomi", "gambar": "assets/Lomi.png"},
            {"nama": "Iqbal", "gambar": "assets/Iqbal.png"},
            {"nama": "Gina", "gambar": "assets/Gina.png"}
        ],
        "lain_lain": None
    },
    "2025-08-02": {
        "hari": "Sabtu",
        "balai_desa": None,
        "masak": None,
        "lain_lain": None
    },
    "2025-08-03": {
        "hari": "Minggu",
        "balai_desa": None,
        "masak": None,
        "lain_lain": None
    }
}

# ==============================================================================
# TATA LETAK / UI (USER INTERFACE)
# ==============================================================================

# Inisialisasi session state untuk menyimpan tab yang aktif
if "toggle" not in st.session_state:
    st.session_state.toggle = "balai" # Default ke tab pertama

# --- PERUBAHAN UNTUK MENAMBAHKAN LOGO DI ATAS JUDUL ---

# Buat dua kolom: satu untuk logo, satu untuk judul
col_logo, col_title = st.columns([1, 5]) # Beri logo 1 bagian, judul 5 bagian

with col_logo:
    # Tampilkan logo Anda. Pastikan path-nya sudah benar.
    # Ganti 'assets/logo.png' dengan path file logo Anda.
    st.image("assets/logo.png", width=100)

with col_title:
    # Tampilkan judul. Gunakan CSS untuk mengatur posisi vertikal.
    st.markdown(
        """
        <div style="height: 100px; display: flex; align-items: center;">
            <h1 style="font-size: 42px; margin: 0;">Dashboard WarTeg!</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

# Beri sedikit spasi setelah header
st.write("") 
# -----------------------------------------------------------

# Pilihan tanggal
from datetime import datetime # Pastikan ini ada di bagian atas file Anda

# --- PERUBAHAN MENGGUNAKAN POPUP KALENDER (st.date_input) ---

# 1. Ubah kunci string tanggal di data Anda menjadi objek tanggal
#    Ini diperlukan untuk menentukan rentang tanggal yang valid di kalender.
available_dates = [datetime.strptime(tgl, "%Y-%m-%d").date() for tgl in jadwal.keys()]

# 2. Tampilkan popup kalender
#    Kita batasi pilihan hanya pada tanggal yang ada di data jadwal.
selected_date_obj = st.date_input(
    "Pilih tanggal",
    value=min(available_dates),      # Tanggal default yang muncul
    min_value=min(available_dates),  # Tanggal paling awal yang bisa dipilih
    max_value=max(available_dates)   # Tanggal paling akhir yang bisa dipilih
)

# 3. Ubah kembali objek tanggal yang dipilih menjadi format string
#    agar bisa digunakan untuk mencari data di dictionary 'jadwal'.
selected_tanggal = selected_date_obj.strftime("%Y-%m-%d")

# 4. Ambil data harian dengan aman
#    Menggunakan .get() untuk menghindari error jika tanggal yang dipilih
#    (misalnya hari libur di tengah rentang) tidak memiliki jadwal.
data_harian = jadwal.get(selected_tanggal)

# -----------------------------------------------------------

# Tampilkan subheader dan konten HANYA JIKA ada jadwal untuk tanggal tersebut
if data_harian:
    st.subheader(f"{data_harian['hari']}, {selected_tanggal}")
    # ... (sisa kode Anda untuk menampilkan tombol dan jadwal)
else:
    st.warning(f"Tidak ada jadwal yang tercatat untuk tanggal {selected_tanggal}.")

data_harian = jadwal[selected_tanggal]

st.write("---")

# Bagian Jadwal Harian
st.markdown("### 📅 Jadwal Harian")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏛️ Balai Desa", use_container_width=True):
        st.session_state.toggle = "balai"
with col2:
    if st.button("🍳 Masak", use_container_width=True):
        st.session_state.toggle = "masak"
with col3:
    if st.button("🍬 Lain-Lain", use_container_width=True):
        st.session_state.toggle = "lain"

# Konten dinamis berdasarkan tombol yang ditekan
# Konten dinamis berdasarkan tombol yang ditekan
if st.session_state.toggle == "balai":
    st.success("👥 Petugas Balai Desa:")
    # Ambil data petugas, gunakan .get() agar lebih aman
    petugas_balai_desa = data_harian.get("balai_desa")

    # Cek jika data ada (tidak None dan tidak kosong)
    if petugas_balai_desa:
        tampilkan_petugas(petugas_balai_desa)
    else:
        # Tampilkan pesan jika None atau list kosong
        st.info("🏖️ Libur")

elif st.session_state.toggle == "masak":
    st.success("👩‍🍳 Petugas Masak:")
    petugas_masak = data_harian.get("masak")

    if petugas_masak:
        tampilkan_petugas(petugas_masak)
    else:
        st.info("🏖️ Libur")

elif st.session_state.toggle == "lain":
    st.info("📌 Jadwal Lain-Lain:")
    jadwal_lain = data_harian.get("lain_lain")

    if jadwal_lain:
        for kegiatan in jadwal_lain:
            st.write(f"- {kegiatan}")
    else:
        st.info("🏖️ Libur / Tidak ada jadwal lain.")

st.markdown("---")

# ==============================================================================
# BAGIAN PROGRAM KERJA (DENGAN TOMBOL HAPUS)
# ==============================================================================

st.markdown("---")
st.markdown("### 📌 Daftar Proker")

# NAMA FILE UNTUK MENYIMPAN DATA
NAMA_FILE_DATA = "data_proker.json"

# DATA DEFAULT JIKA FILE TIDAK DITEMUKAN
DATA_DEFAULT = [
    {
        "judul": "Kandaga",
        "catatan": "Budidaya Ikan dalam Galon",
        "subkegiatan": [
            {"task": "Beli EM4", "checked": False},
            {"task": "Beli Plastik", "checked": False},
            {"task": "Beli Media Tanam", "checked": False},
            {"task": "Beli Selang", "checked": False},
            {"task": "Galon", "checked": False},
            {"task": "Sewa Alat", "checked": False},
            {"task": "Pengendapan Air", "checked": False},
            {"task": "Rakit Media", "checked": False},
            {"task": "Beli Bibit", "checked": False},
            {"task": "Barang Jadi (Trial)", "checked": False},
            {"task": "Demonstrasi 1", "checked": False},
            {"task": "Demonstrasi 2", "checked": False}
        ],
    },
    {
        "judul": "TandurKit",
        "catatan": "Kit/Starter Pack Penanaman untuk Anak",
        "subkegiatan": [
            {"task": "Beli Bahan", "checked": False},
            {"task": "Isi Kit", "checked": False},
            {"task": "Demonstrasi", "checked": False}
        ],
    }
]

# --- FUNGSI UNTUK MEMBACA, MENYIMPAN, DAN MENGHAPUS DATA ---

def simpan_data(data):
    """Menyimpan data proker ke file JSON."""
    with open(NAMA_FILE_DATA, 'w') as f:
        json.dump(data, f, indent=4)

def muat_data():
    """Memuat data proker dari file JSON. Jika file tidak ada, buat baru."""
    try:
        with open(NAMA_FILE_DATA, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        simpan_data(DATA_DEFAULT)
        return DATA_DEFAULT

# --- FUNGSI UNTUK MENGHAPUS SUB-KEGIATAN ---
def hapus_sub_kegiatan(index_proker, index_sub_kegiatan):
    """Menghapus sebuah sub-kegiatan dari proker tertentu."""
    del st.session_state.proker[index_proker]['subkegiatan'][index_sub_kegiatan]
    simpan_data(st.session_state.proker) # Simpan perubahan ke file
    # st.rerun() tidak perlu dipanggil di sini karena on_click akan memicu rerun

# --- LOGIKA UTAMA ---

# Muat data ke session_state saat aplikasi pertama kali dijalankan
if 'proker' not in st.session_state:
    st.session_state.proker = muat_data()

# Form untuk menambah Program Kerja (Proker) baru
with st.form("form_proker_baru", clear_on_submit=True):
    st.write("**Tambah Program Kerja Baru**")
    judul_baru = st.text_input("Judul Proker")
    catatan_baru = st.text_input("Catatan Proker (opsional)")
    submitted = st.form_submit_button("➕ Tambah Proker")

    if submitted and judul_baru:
        st.session_state.proker.append({
            "judul": judul_baru,
            "catatan": catatan_baru,
            "subkegiatan": []
        })
        simpan_data(st.session_state.proker)
        st.success(f"Proker '{judul_baru}' berhasil ditambahkan!")
        st.rerun()

st.write("---")

# Fungsi untuk menambah sub-kegiatan (dengan penyimpanan)
def tambah_sub_kegiatan(index_proker, nama_sub_kegiatan):
    if nama_sub_kegiatan:
        st.session_state.proker[index_proker]['subkegiatan'].append(
            {"task": nama_sub_kegiatan, "checked": False}
        )
        simpan_data(st.session_state.proker)

# Tampilkan semua proker dari session_state
for idx, pk in enumerate(st.session_state.proker):
    with st.expander(f"{pk['judul']}"):
        st.write(f"📎 Catatan: {pk['catatan']}")

        # Tampilkan dan proses setiap sub-kegiatan
        ada_perubahan_checkbox = False
        for i, sub in enumerate(pk["subkegiatan"]):
            # Buat kolom untuk checkbox dan tombol hapus
            col_task, col_delete = st.columns([0.9, 0.1], gap="small")

            with col_task:
                is_checked_sekarang = st.checkbox(
                    sub['task'],
                    value=sub['checked'],
                    key=f"proker_{idx}_{i}"
                )
                if st.session_state.proker[idx]['subkegiatan'][i]['checked'] != is_checked_sekarang:
                    st.session_state.proker[idx]['subkegiatan'][i]['checked'] = is_checked_sekarang
                    ada_perubahan_checkbox = True

            with col_delete:
                st.button(
                    "🗑️",
                    key=f"delete_{idx}_{i}",
                    on_click=hapus_sub_kegiatan,
                    args=(idx, i), # Kirim index proker dan index sub-kegiatan
                    help="Hapus sub-kegiatan ini" # Tooltip saat mouse diarahkan ke tombol
                )

        if ada_perubahan_checkbox:
            simpan_data(st.session_state.proker)
            st.rerun()

        # Hitung progress bar
        if pk["subkegiatan"]:
            checks = [sub['checked'] for sub in pk['subkegiatan']]
            persen = sum(checks) / len(checks)
            st.progress(persen)
            st.caption(f"{persen:.0%} selesai")
        else:
            st.caption("Belum ada sub-kegiatan.")

        st.write("")

        # Input untuk menambah sub-kegiatan baru
        st.write("**Tambah Sub-Kegiatan:**")
        input_sub = st.text_input("Ketik sub-kegiatan baru", key=f"input_sub_{idx}", label_visibility="collapsed")
        st.button("➕ Tambah", key=f"tambah_sub_{idx}", on_click=tambah_sub_kegiatan, args=(idx, input_sub))


# ==============================================================================
# SECTION BARU: LIST BELANJA (V2 - DENGAN TOPIK)
# ==============================================================================

st.markdown("---")
st.markdown("### 🛒 List Belanja")

# --- KONFIGURASI & FUNGSI UNTUK LIST BELANJA ---
NAMA_FILE_BELANJA = "data_belanja.json"

def simpan_data_belanja(data):
    with open(NAMA_FILE_BELANJA, 'w') as f: json.dump(data, f, indent=4)

def muat_data_belanja():
    try:
        with open(NAMA_FILE_BELANJA, 'r') as f: return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def tambah_topik_belanja(judul_topik):
    if judul_topik:
        st.session_state.list_belanja.append({"judul": judul_topik, "items": []})
        simpan_data_belanja(st.session_state.list_belanja)

def hapus_topik_belanja(index_topik):
    del st.session_state.list_belanja[index_topik]
    simpan_data_belanja(st.session_state.list_belanja)

def tambah_item_belanja(index_topik, nama_item):
    if nama_item:
        st.session_state.list_belanja[index_topik]['items'].append({"task": nama_item, "checked": False})
        simpan_data_belanja(st.session_state.list_belanja)

def hapus_item_belanja(index_topik, index_item):
    del st.session_state.list_belanja[index_topik]['items'][index_item]
    simpan_data_belanja(st.session_state.list_belanja)

if 'list_belanja' not in st.session_state:
    st.session_state.list_belanja = muat_data_belanja()

# --- UI UNTUK LIST BELANJA ---

# 1. Form untuk menambah TOPIK BELANJA BARU
with st.form("form_topik_belanja_baru", clear_on_submit=True):
    st.write("**Tambah Topik Keperluan Baru**")
    judul_topik_baru = st.text_input("Judul Topik (misal: Belanja Dapur, Keperluan POC)")
    if st.form_submit_button("➕ Tambah Topik"):
        tambah_topik_belanja(judul_topik_baru)
        st.success(f"Topik '{judul_topik_baru}' berhasil ditambahkan!")
        st.rerun()

st.write("---")

# 2. Tampilkan setiap TOPIK BELANJA dalam expander
for idx, topik in enumerate(st.session_state.list_belanja):
    with st.expander(f"{topik['judul']}"):
        
        # 3. Tampilkan setiap ITEM BELANJA di dalam topik
        ada_perubahan_check_belanja = False
        for i, item in enumerate(topik["items"]):
            col_item, col_delete_item = st.columns([0.9, 0.1], gap="small")
            with col_item:
                is_checked = st.checkbox(item['task'], value=item['checked'], key=f"belanja_{idx}_item_{i}")
                if st.session_state.list_belanja[idx]['items'][i]['checked'] != is_checked:
                    st.session_state.list_belanja[idx]['items'][i]['checked'] = is_checked
                    ada_perubahan_check_belanja = True
            with col_delete_item:
                st.button("🗑️", key=f"hapus_belanja_{idx}_item_{i}", on_click=hapus_item_belanja, args=(idx, i), help="Hapus barang ini")

        if ada_perubahan_check_belanja:
            simpan_data_belanja(st.session_state.list_belanja)
            st.rerun()

        # 4. Input untuk menambah ITEM BARU di dalam topik ini
        st.write("")
        input_item_baru = st.text_input("Tambah barang ke list ini...", key=f"input_belanja_{idx}", label_visibility="collapsed")
        st.button("➕ Tambah Barang", key=f"tambah_belanja_item_{idx}", on_click=tambah_item_belanja, args=(idx, input_item_baru))

        st.divider()
        # 5. Tombol untuk menghapus SELURUH TOPIK BELANJA
        st.button("❌ Hapus Semua List", key=f"hapus_topik_{idx}", on_click=hapus_topik_belanja, args=(idx,))
