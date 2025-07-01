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
    Menampilkan daftar petugas dalam layout DUA KOLOM yang dipaksa (forced)
    menggunakan HTML Flexbox, bahkan di mobile.
    """
    # Memulai container flexbox.
    all_items_html = '<div style="display: flex; flex-wrap: wrap; justify-content: space-between;">'

    for orang in daftar_petugas:
        # Panggil fungsi render untuk mendapatkan string HTML satu item
        # dan tambahkan ke string utama.
        all_items_html += render_satu_petugas(orang)

    # Tutup tag div container
    all_items_html += '</div>'

    # Render seluruh blok HTML sekaligus
    st.markdown(all_items_html, unsafe_allow_html=True)


def render_satu_petugas(orang: dict) -> str:
    """
    Fungsi ini bertanggung jawab untuk me-render SATU item petugas
    dan MENGEMBALIKANNYA SEBAGAI STRING HTML.
    """
    base64_image = get_image_as_base64(orang["gambar"])
    
    # Style untuk setiap item. 'flex: 0 0 48%' adalah kunci untuk 2 kolom.
    item_style = "flex: 0 0 48%; display: flex; flex-direction: column; align-items: center; margin-bottom: 20px;"

    if base64_image:
        # Menggunakan HTML untuk layout yang lebih ringkas dan terpusat
        item_html = f"""
            <div style="{item_style}">
                <img src="data:image/png;base64,{base64_image}"
                     style="
                        width: 80px;
                        height: 80px;
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
        return item_html
    else:
        # Placeholder jika gambar tidak ditemukan
        placeholder_html = f"""
            <div style="{item_style}">
                <div style="width:80px; height:80px; background-color:#ddd; border-radius:50%;"></div>
                <div style="font-weight: bold; text-align: center; margin-top: 8px;">{orang['nama']}</div>
            </div>
        """
        return placeholder_html


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
            {"nama": "Deni", "gambar": "assets/Deni.png"},
            {"nama": "Via", "gambar": "assets/Via.png"},
            {"nama": "Lomi", "gambar": "assets/Lomi.png"}
        ],
        "lain_lain": ["Koordinasi RW"]
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
tanggal_list = list(jadwal.keys())
selected_tanggal = st.selectbox("Pilih tanggal", tanggal_list)
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
