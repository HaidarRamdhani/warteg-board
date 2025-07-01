import streamlit as st
from datetime import date
import os

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard WarTeg", layout="wide")

# ===================== Dummy Data =====================
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
    },
    {
        "judul": "Pelatihan UMKM",
        "catatan": "Siapkan modul dan daftar peserta",
        "subkegiatan": ["Draft modul", "Cetak sertifikat", "Pesan konsumsi"],
    }
]

# ===================== Inisialisasi State =====================
if "show" not in st.session_state:
    st.session_state.show = {"balai": False, "masak": False, "lain": False}

# ===================== Pilih Tanggal =====================
st.markdown("<h1>📅 Dashboard WarTeg!</h1>", unsafe_allow_html=True)
tanggal_list = list(jadwal.keys())
selected_tanggal = st.selectbox("Pilih tanggal", tanggal_list)
data_harian = jadwal[selected_tanggal]
st.subheader(f"{data_harian['hari']}, {selected_tanggal}")
st.divider()

# ===================== Gambar jadi tombol =====================
st.markdown("### Jadwal Harian")

col1, col2, col3 = st.columns(3)

def display_icon_with_button(col, key, img_path, label):
    with col:
        st.image(img_path, width=100)
        if st.button(label, key=f"btn_{key}"):
            st.session_state.show[key] = not st.session_state.show[key]

display_icon_with_button(col1, "balai", "assets/balai_desa.png", "Balai Desa")
display_icon_with_button(col2, "masak", "assets/masak.png", "Masak")
display_icon_with_button(col3, "lain", "assets/lain_lain.png", "Lain-Lain")

# ===================== Tampilkan Petugas =====================
if st.session_state.show["balai"]:
    st.success("👥 Petugas Balai Desa:")
    for nama in data_harian["balai_desa"]:
        st.write(f"- {nama}")

if st.session_state.show["masak"]:
    st.success("👩‍🍳 Petugas Masak:")
    for nama in data_harian["masak"]:
        st.write(f"- {nama}")

if st.session_state.show["lain"]:
    st.warning("🕒 Jadwal Lain-Lain:")
    if data_harian["lain_lain"]:
        for item in data_harian["lain_lain"]:
            st.write(f"- {item}")
    else:
        st.write("Belum ada jadwal.")

st.divider()

# ===================== Daftar Proker =====================
st.markdown("### 📌 Daftar Proker")

for idx, pk in enumerate(proker):
    with st.expander(pk["judul"]):
        st.write(f"📎 *Catatan:* {pk['catatan']}")
        checks = [st.checkbox(sub, key=f"{idx}-{i}") for i, sub in enumerate(pk["subkegiatan"])]
        persen = sum(checks) / len(checks) * 100
        st.progress(persen / 100)
        st.caption(f"{persen:.0f}% selesai")
