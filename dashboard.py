import streamlit as st
import base64
from datetime import date

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

# Data program kerja
proker = [
    {
        "judul": "Penyuluhan Gizi",
        "catatan": "Hubungi puskesmas & siapkan materi",
        "subkegiatan": ["Hubungi narasumber", "Desain pamflet", "Cetak materi"],
    },
    {
        "judul": "Pelatihan Digital",
        "catatan": "Pastikan sinyal & LCD tersedia",
        "subkegiatan": ["Survey peserta", "Siapkan modul", "Latihan presentasi"],
    }
]

# ==============================================================================
# TATA LETAK / UI (USER INTERFACE)
# ==============================================================================

# Inisialisasi session state untuk menyimpan tab yang aktif
if "toggle" not in st.session_state:
    st.session_state.toggle = "balai" # Default ke tab pertama

# Header utama
st.markdown(f"<h1 style='font-size: 42px;'>📅 Dashboard WarTeg!</h1>", unsafe_allow_html=True)

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
st.markdown("### Jadwal Harian")

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

# Bagian Program Kerja
st.markdown("### 📌 Daftar Proker")
for idx, pk in enumerate(proker):
    with st.expander(f"{pk['judul']}"):
        st.write(f"📎 Catatan: {pk['catatan']}")
        checks = [st.checkbox(f"{item}", key=f"proker_{idx}_{i}") for i, item in enumerate(pk["subkegiatan"])]
        if checks:
            persen = sum(checks) / len(checks)
            st.progress(persen)
            st.caption(f"{persen:.0%} selesai")
        else:
            st.caption("Tidak ada sub-kegiatan.")
