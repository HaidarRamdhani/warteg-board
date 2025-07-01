import streamlit as st
import base64
from datetime import date

# ================== Setup ==================
st.set_page_config(page_title="Dashboard WarTeg", layout="wide")

# ================== Dummy Data ==================
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

# ================== Pilih Tanggal ==================
st.markdown("<h1>📅 Dashboard WarTeg!</h1>", unsafe_allow_html=True)
tanggal_list = list(jadwal.keys())
selected_tanggal = st.selectbox("Pilih tanggal", tanggal_list)
data_harian = jadwal[selected_tanggal]
st.subheader(f"{data_harian['hari']}, {selected_tanggal}")
st.divider()

# ================== Inisialisasi State ==================
if "show" not in st.session_state:
    st.session_state.show = {"balai": False, "masak": False, "lain": False}

# ================== Gambar jadi tombol ==================
def get_base64(img_path):
    with open(img_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def clickable_image(col, key, img_path, label):
    img_b64 = get_base64(img_path)
    btn_key = f"btn_{key}"

    button_html = f"""
        <div style="text-align:center;">
            <form action="" method="post">
                <button name="{btn_key}" type="submit" style="background: none; border: none;">
                    <img src="data:image/png;base64,{img_b64}" width="100"/>
                </button>
                <p style="margin-top: 0.3rem;">{label}</p>
            </form>
        </div>
    """
    with col:
        st.markdown(button_html, unsafe_allow_html=True)
        if st.session_state.get(btn_key):
            st.session_state.show[key] = not st.session_state.show[key]

# Force init tombol klik
for k in ["btn_balai", "btn_masak", "btn_lain"]:
    if k not in st.session_state:
        st.session_state[k] = False

# ================== Ikon Jadwal Harian ==================
st.markdown("### Jadwal Harian")
col1, col2, col3 = st.columns(3)
clickable_image(col1, "balai", "assets/balai_desa.png", "Balai Desa")
clickable_image(col2, "masak", "assets/masak.png", "Masak")
clickable_image(col3, "lain", "assets/lain_lain.png", "Lain-Lain")

# ================== Tampilkan Konten Setelah Diklik ==================
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

# ================== Daftar Proker ==================
st.markdown("### 📌 Daftar Proker")
for idx, pk in enumerate(proker):
    with st.expander(pk["judul"]):
        st.write(f"📎 *Catatan:* {pk['catatan']}")
        checks = [st.checkbox(sub, key=f"{idx}-{i}") for i, sub in enumerate(pk["subkegiatan"])]
        persen = sum(checks) / len(checks) * 100
        st.progress(persen / 100)
        st.caption(f"{persen:.0f}% selesai")
