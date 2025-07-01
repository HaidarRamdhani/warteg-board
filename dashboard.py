import streamlit as st
from datetime import date

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard WarTeg", layout="wide")

# Data jadwal menggunakan path lokal dari folder 'assets'
# Pastikan folder 'assets' ada di repository GitHub Anda.
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

# Inisialisasi session state
if "toggle" not in st.session_state:
    st.session_state.toggle = None

# ---- UI (User Interface) ----

# Pilihan tanggal
tanggal_list = list(jadwal.keys())
selected_tanggal = st.selectbox("Pilih tanggal", tanggal_list)
data_harian = jadwal[selected_tanggal]

# Header
st.markdown(f"<h1 style='font-size: 42px;'>📅 Dashboard WarTeg!</h1>", unsafe_allow_html=True)
st.subheader(f"{data_harian['hari']}, {selected_tanggal}")
st.write("---")

# Bagian Jadwal Harian
st.markdown("### Jadwal Harian")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏛️\nBalai Desa", use_container_width=True):
        st.session_state.toggle = "balai"

with col2:
    if st.button("🍳\nMasak", use_container_width=True):
        st.session_state.toggle = "masak"

with col3:
    if st.button("🍬\nLain-Lain", use_container_width=True):
        st.session_state.toggle = "lain"

def tampilkan_petugas(daftar_petugas):
    for orang in daftar_petugas:
        # 1. Perkecil jarak antar kolom dengan `gap="small"`
        # 2. Sesuaikan rasio kolom agar lebih pas
        col_img, col_nama = st.columns([1, 5], gap="small")

        with col_img:
            # Tetapkan lebar gambar ke 64px. Ini ukuran yang baik untuk ikon.
            # Browser akan melakukan downscaling ke ukuran ini.
            st.image(orang["gambar"], width=250)

        with col_nama:
            # Trik CSS untuk membuat nama berada di tengah secara vertikal
            # dan menghilangkan margin default dari tag header.
            st.markdown(
                f"""
                <div style="height: 64px; display: flex; align-items: center;">
                    <h5 style="margin: 0; padding-left: 10px;">{orang['nama']}</h5>
                </div>
                """,
                unsafe_allow_html=True
            )
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
