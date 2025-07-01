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
# --- PERUBAHAN UNTUK MENAMBAHKAN NAMA HARI DI SELECTBOX ---
# Ambil daftar tanggal (kunci dari dictionary)
tanggal_list = list(jadwal.keys())

# Buat fungsi untuk memformat tampilan di selectbox
def format_nama_hari(tanggal):
    nama_hari = jadwal[tanggal]['hari']
    return f"{nama_hari}, {tanggal}"

# Gunakan format_func di st.selectbox
selected_tanggal = st.selectbox(
    "Pilih tanggal",
    options=tanggal_list,
    format_func=format_nama_hari
)
# -----------------------------------------------------------

data_harian = jadwal[selected_tanggal]

st.subheader(f"{data_harian['hari']}, {selected_tanggal}")
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
if st.session_state.toggle == "balai":
    st.success("👥 Petugas Balai Desa:")
    tampilkan_petugas(data_harian["balai_desa"])
elif st.session_state.toggle == "masak":
    st.success("👩‍🍳 Petugas Masak:")
    tampilkan_petugas(data_harian["masak"])
elif st.session_state.toggle == "lain":
    st.info("📌 Jadwal Lain-Lain:")
    if data_harian["lain_lain"]:
        for kegiatan in data_harian["lain_lain"]:
            st.write(f"- {kegiatan}")
    else:
        st.write("Belum ada jadwal lain.")

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
