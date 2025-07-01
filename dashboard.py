import streamlit as st
import datetime
import json

# Dummy data jadwal
jadwal = {
    "2025-07-01": {
        "hari": "Selasa",
        "balai_desa": ["Haidar", "Salsa"],
        "masak": ["Ani", "Budi", "Citra", "Dedi"]
    },
    "2025-07-02": {
        "hari": "Rabu",
        "balai_desa": ["Dina", "Eko"],
        "masak": ["Fina", "Gilang", "Hana", "Ivan"]
    }
}

# Dummy data proker
proker = [
    {
        "judul": "Penyuluhan Gizi",
        "catatan": "Hubungi puskesmas & siapkan materi",
        "subkegiatan": ["Hubungi narasumber", "Desain pamflet", "Cetak materi"],
    }
]

# Sidebar tanggal
tanggal_list = list(jadwal.keys())
selected_tanggal = st.selectbox("Pilih tanggal", tanggal_list)
data_harian = jadwal[selected_tanggal]

st.title("📅 Dashboard WarTeg!")
st.header(f"{data_harian['hari']}, {selected_tanggal}")

# Jadwal
with st.expander("📍 Jadwal Balai Desa"):
    for nama in data_harian["balai_desa"]:
        st.write(f"- {nama}")

with st.expander("🍳 Jadwal Masak"):
    for nama in data_harian["masak"]:
        st.write(f"- {nama}")

# Proker
st.subheader("📌 Daftar Proker")

for idx, pk in enumerate(proker):
    with st.expander(f"{pk['judul']}"):
        st.write(f"📎 Catatan: {pk['catatan']}")
        checks = [st.checkbox(f"{item}", key=f"{idx}-{i}") for i, item in enumerate(pk["subkegiatan"])]
        persen = sum(checks) / len(checks) * 100
        st.progress(persen / 100)
        st.caption(f"{persen:.0f}% selesai")

