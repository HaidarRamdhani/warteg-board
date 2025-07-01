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
    }
]


# Pilih tanggal
tanggal_list = list(jadwal.keys())
selected_tanggal = st.selectbox("Pilih tanggal", tanggal_list)
data_harian = jadwal[selected_tanggal]

# Header
st.markdown(f"<h1 style='font-size: 42px;'>📅 Dashboard WarTeg!</h1>", unsafe_allow_html=True)
st.subheader(f"{data_harian['hari']}, {selected_tanggal}")

st.write("---")

# Gaya ikon tombol
st.markdown("""
<style>
.button-icon {
    display: flex;
    justify-content: space-evenly;
    margin-bottom: 1rem;
}
.button-style {
    background-color: #a3e635;
    border-radius: 50%;
    width: 90px;
    height: 90px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 32px;
    font-weight: bold;
    cursor: pointer;
    transition: 0.2s ease-in-out;
}
.button-style:hover {
    transform: scale(1.1);
}
</style>
""", unsafe_allow_html=True)

# Tombol Icon
col1, col2, col3 = st.columns(3)
show_balai = col1.button("🏢 Balai Desa")
show_masak = col2.button("🍳 Masak")
show_lain = col3.button("🍬 Lain-Lain")

# Konten muncul setelah ditekan
if show_balai:
    st.success("Petugas Balai Desa:")
    for nama in data_harian["balai_desa"]:
        st.write(f"- {nama}")

if show_masak:
    st.success("Petugas Masak:")
    for nama in data_harian["masak"]:
        st.write(f"- {nama}")

if show_lain:
    st.warning("Jadwal Lain-Lain:")
    if data_harian["lain_lain"]:
        for nama in data_harian["lain_lain"]:
            st.write(f"- {nama}")
    else:
        st.write("Belum ada jadwal.")

# Proker
st.subheader("📌 Daftar Proker")

for idx, pk in enumerate(proker):
    with st.expander(f"{pk['judul']}"):
        st.write(f"📎 Catatan: {pk['catatan']}")
        checks = [st.checkbox(f"{item}", key=f"{idx}-{i}") for i, item in enumerate(pk["subkegiatan"])]
        persen = sum(checks) / len(checks) * 100
        st.progress(persen / 100)
        st.caption(f"{persen:.0f}% selesai")


