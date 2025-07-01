import streamlit as st
from datetime import date

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard WarTeg", layout="wide")

# Dummy data jadwal
jadwal = {
    "2025-07-01": {
        "hari": "Selasa",
        "balai_desa": ["Haidar", "Salsa"],
        "masak": ["Ani", "Budi", "Citra", "Dedi"],
        "lain_lain": None
    },
    "2025-07-02": {
        "hari": "Rabu",
        "balai_desa": ["Dina", "Eko"],
        "masak": ["Fina", "Gilang", "Hana", "Ivan"],
        "lain_lain": ["Koordinasi RW"]
    }
}

# Dummy data proker
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

# Inisialisasi toggle jika belum ada
if "toggle" not in st.session_state:
    st.session_state.toggle = None

# Pilih tanggal
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

# Konten berdasarkan tombol yang ditekan
if st.session_state.toggle == "balai":
    st.success("👥 Petugas Balai Desa:")
    for nama in data_harian["balai_desa"]:
        st.write(f"- {nama}")

elif st.session_state.toggle == "masak":
    st.success("👩‍🍳 Petugas Masak:")
    for nama in data_harian["masak"]:
        st.write(f"- {nama}")

elif st.session_state.toggle == "lain":
    st.info("📌 Jadwal Lain-Lain:")
    if data_harian["lain_lain"]:
        for kegiatan in data_harian["lain_lain"]:
            st.write(f"- {kegiatan}")
    else:
        st.write("Belum ada jadwal.")

st.markdown("---")

# Bagian Proker
st.markdown("### 📌 Daftar Proker")

for idx, pk in enumerate(proker):
    with st.expander(f"{pk['judul']}"):
        st.write(f"📎 Catatan: {pk['catatan']}")
        checks = [st.checkbox(f"{item}", key=f"{idx}-{i}") for i, item in enumerate(pk["subkegiatan"])]
        persen = sum(checks) / len(checks) * 100
        st.progress(persen / 100)
        st.caption(f"{persen:.0f}% selesai")
