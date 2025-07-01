import streamlit as st
from datetime import date

st.set_page_config(page_title="Dashboard WarTeg", layout="wide")

# ==================== DATA DUMMY ==================== #
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

# ==================== STATE ==================== #
if "toggle" not in st.session_state:
    st.session_state.toggle = {"balai": False, "masak": False, "lain": False}

# ==================== TANGGAL ==================== #
tanggal = st.selectbox("Pilih tanggal", list(jadwal.keys()))
data = jadwal[tanggal]

st.markdown(f"## 📅 Dashboard WarTeg!")
st.subheader(f"{data['hari']}, {tanggal}")
st.divider()

# ==================== STYLING ==================== #
st.markdown("""
<style>
.icon-button {
    border: none;
    background: transparent;
    cursor: pointer;
    text-align: center;
}
.icon-button img {
    width: 100px;
    transition: 0.2s ease-in-out;
}
.icon-button img:hover {
    transform: scale(1.1);
}
.icon-grid {
    display: flex;
    justify-content: space-evenly;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# ==================== IKON (GAMBAR = TOMBOL) ==================== #
st.markdown("### Jadwal Harian")

# Event click manual
params = st.query_params
if "klik" in params:
    klik = params["klik"]
    st.session_state.toggle[klik] = not st.session_state.toggle[klik]

# HTML dengan link query string untuk trigger toggle
st.markdown(f"""
<div class="icon-grid">
    <a href="?klik=balai" class="icon-button"><img src="https://img.icons8.com/ios-filled/100/museum.png" title="Balai Desa" /></a>
    <a href="?klik=masak" class="icon-button"><img src="https://img.icons8.com/ios/100/cooking-pot.png" title="Masak" /></a>
    <a href="?klik=lain" class="icon-button"><img src="https://img.icons8.com/ios/100/more.png" title="Lain-Lain" /></a>
</div>
""", unsafe_allow_html=True)

# ==================== KONTEN ==================== #
if st.session_state.toggle["balai"]:
    st.success("👥 Petugas Balai Desa:")
    for nama in data["balai_desa"]:
        st.write(f"- {nama}")

if st.session_state.toggle["masak"]:
    st.success("👩‍🍳 Petugas Masak:")
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

# ==================== PROKER ==================== #
st.markdown("### 📌 Daftar Proker")
for idx, p in enumerate(proker):
    with st.expander(p["judul"]):
        st.write(f"📎 Catatan: {p['catatan']}")
        checks = [st.checkbox(x, key=f"{idx}-{i}") for i, x in enumerate(p["subkegiatan"])]
        percent = sum(checks) / len(checks) * 100
        st.progress(percent / 100)
        st.caption(f"{percent:.0f}% selesai")
