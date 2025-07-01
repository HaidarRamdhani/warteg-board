import streamlit as st
from PIL import Image
from datetime import date

# ================== Konfigurasi Halaman ==================
st.set_page_config(page_title="Dashboard WarTeg", layout="wide")

# ================== Data Dummy ==================
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

proker = [
    {
        "judul": "Penyuluhan Gizi",
        "catatan": "Hubungi puskesmas & siapkan materi",
        "subkegiatan": ["Hubungi narasumber", "Desain pamflet", "Cetak materi"],
    }
]

# ================== Header ==================
st.markdown("<h1 style='font-size: 42px;'>📅 Dashboard WarTeg!</h1>", unsafe_allow_html=True)

tanggal_list = list(jadwal.keys())
selected_tanggal = st.selectbox("Pilih tanggal", tanggal_list)
data_harian = jadwal[selected_tanggal]
st.subheader(f"{data_harian['hari']}, {selected_tanggal}")
st.write("---")

# ================== Inisialisasi State ==================
if "show" not in st.session_state:
    st.session_state.show = {"balai": False, "masak": False, "lain": False}

def toggle(key):
    st.session_state.show[key] = not st.session_state.show[key]

# ================== Tampilan Ikon Jadwal ==================
st.markdown("### Jadwal Harian")
col1, col2, col3 = st.columns(3)

with col1:
    st.image("assets/balai_desa.svg", width=100)
    if st.button("Balai Desa"):
        toggle("balai")

with col2:
    st.image("assets/masak.svg", width=100)
    if st.button("Masak"):
        toggle("masak")

with col3:
    st.image("assets/lain_lain.svg", width=100)
    if st.button("Lain-Lain"):
        toggle("lain")

# ================== Konten Muncul Setelah Klik ==================
if st.session_state.show["balai"]:
    st.success("👥 Petugas Balai Desa:")
    for nama in data_harian["balai_desa"]:
        st.write(f"- {nama}")

if st.session_state.show["masak"]:
    st.success("👩‍🍳 Petugas Masak:")
    for nama in data_harian["masak"]:
        st.write(f"- {nama}")

if st.session_state.show["lain"]:
    st.warning("🕒 Jadwal Lain-lain:")
    if data_harian["lain_lain"]:
        for item in data_harian["lain_lain"]:
            st.write(f"- {item}")
    else:
        st.write("Belum ada jadwal.")

st.write("---")

# ================== Tampilan Progress Proker ==================
st.subheader("📌 Daftar Proker")

for idx, pk in enumerate(proker):
    with st.expander(f"{pk['judul']}"):
        st.write(f"📎 Catatan: {pk['catatan']}")
        checks = [st.checkbox(f"{item}", key=f"{idx}-{i}") for i, item in enumerate(pk["subkegiatan"])]
        persen = sum(checks) / len(checks) * 100
        st.progress(persen / 100)
        st.caption(f"{persen:.0f}% selesai")
