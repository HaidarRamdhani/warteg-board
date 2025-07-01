import streamlit as st
from datetime import date

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard WarTeg", layout="wide")

# Dummy jadwal
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

# Dummy proker
proker = [
    {
        "judul": "Penyuluhan Gizi",
        "catatan": "Hubungi puskesmas & siapkan materi",
        "subkegiatan": ["Hubungi narasumber", "Desain pamflet", "Cetak materi"],
    }
]

# Init state
if "toggle" not in st.session_state:
    st.session_state.toggle = {"balai": False, "masak": False, "lain": False}

# Tanggal
tanggal = st.selectbox("Pilih tanggal", list(jadwal.keys()))
data = jadwal[tanggal]

st.markdown(f"## 📅 Dashboard WarTeg!")
st.subheader(f"{data['hari']}, {tanggal}")
st.divider()

# Bagian ikon
st.markdown("### Jadwal Harian")

col1, col2, col3 = st.columns(3)

with col1:
    st.image("assets/balai_desa.png", width=100)
    if st.button("Balai Desa"):
        st.session_state.toggle["balai"] = not st.session_state.toggle["balai"]

with col2:
    st.image("assets/masak.png", width=100)
    if st.button("Masak"):
        st.session_state.toggle["masak"] = not st.session_state.toggle["masak"]

with col3:
    st.image("assets/lain_lain.png", width=100)
    if st.button("Lain-Lain"):
        st.session_state.toggle["lain"] = not st.session_state.toggle["lain"]

# Konten toggle
if st.session_state.toggle["balai"]:
    st.success("👥 Petugas Balai Desa:")
    for nama in data["balai_desa"]:
        st.write(f"- {nama}")

if st.session_state.toggle["masak"]:
    st.success("👨‍🍳 Petugas Masak:")
    for nama in data["masak"]:
        st.write(f"- {nama}")

if st.session_state.toggle["lain"]:
    st.warning("📌 Jadwal Lain-Lain:")
    if data["lain_lain"]:
        for item in data["lain_lain"]:
            st.write(f"- {item}")
    else:
        st.write("Belum ada jadwal.")

st.divider()

# Proker
st.markdown("### 📌 Daftar Proker")
for idx, p in enumerate(proker):
    with st.expander(p["judul"]):
        st.write(f"📎 Catatan: {p['catatan']}")
        checks = [st.checkbox(x, key=f"{idx}-{i}") for i, x in enumerate(p["subkegiatan"])]
        percent = sum(checks) / len(checks) * 100
        st.progress(percent / 100)
        st.caption(f"{percent:.0f}% selesai")
