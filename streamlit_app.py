import streamlit as st
import pubchempy as pcp
import py3Dmol
from stmol import showmol
import random

# Konfigurasi Halaman
st.set_page_config(page_title="Tata Penamaan Senyawa Organik", layout="wide")

# Database sederhana untuk simulasi reaksi (Bisa diperluas sesuai kebutuhan lab)
REACTION_DATABASE = {
    frozenset(["acetic acid", "ethanol"]): {
        "produk": "ethyl acetate",
        "jenis_reaksi": "Esterifikasi (Kondensasi)",
        "penjelasan": "Reaksi antara asam karboksilat dan alkohol menghasilkan ester dan air, biasanya dikatalisis oleh asam kuat."
    },
    frozenset(["asam asetat", "etanol"]): {
        "produk": "ethyl acetate",
        "jenis_reaksi": "Esterifikasi (Kondensasi)",
        "penjelasan": "Reaksi antara asam karboksilat dan alkohol menghasilkan ester dan air, biasanya dikatalisis oleh asam kuat."
    }
}

# Database Kuis
QUIZ_DATA = [
    {"cid": 241, "nama_iupac": "benzene", "nama_trivial": "bensol"},
    {"cid": 297, "nama_iupac": "methane", "nama_trivial": "gas rawa"},
    {"cid": 176, "nama_iupac": "acetic acid", "nama_trivial": "asam cuka"},
    {"cid": 702, "nama_iupac": "ethanol", "nama_trivial": "alkohol"}
]

def render_3d_molecule(cid):
    """Menghasilkan visualisasi 3D dari PubChem CID"""
    view = py3Dmol.view(query=f'cid:{cid}')
    view.setStyle({'stick': {}})
    view.setBackgroundColor('white')
    view.zoomTo()
    showmol(view, height=400, width=500)

def get_compound_data(compound_name):
    """Mengambil data senyawa dari PubChem"""
    try:
        results = pcp.get_compounds(compound_name, 'name')
        if results:
            return results[0]
        return None
    except:
        return None

# --- UI Aplikasi ---
st.title("Tata Penamaan Senyawa Organik")
st.caption("Dikembangkan oleh Agung Nugraha - Eksplorasi Struktur, Sifat Fisikokimia, dan Reaksi Senyawa")

menu = st.sidebar.radio("Navigasi Menu", ["Eksplorasi & Reaksi", "Latihan Soal"])

if menu == "Eksplorasi & Reaksi":
    st.header("🔍 Pencarian Senyawa Organik")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        senyawa_1 = st.text_input("Masukkan Nama Senyawa (IUPAC / Trivial) - disarankan bahasa Inggris:")
        if senyawa_1:
            comp_1 = get_compound_data(senyawa_1)
            if comp_1:
                st.success(f"Senyawa ditemukan: {comp_1.iupac_name}")
                st.write("**Sifat Fisika & Kimia:**")
                st.write(f"- Berat Molekul: {comp_1.molecular_weight} g/mol")
                st.write(f"- Rumus Molekul: {comp_1.molecular_formula}")
                st.write(f"- Isomeric SMILES: {comp_1.isomeric_smiles}")
                
                st.write("**Struktur 3D:**")
                render_3d_molecule(comp_1.cid)
            else:
                st.error("Senyawa tidak ditemukan di database PubChem.")

    with col2:
        st.subheader("🧪 Reaksikan Senyawa")
        reaksikan = st.checkbox("Tambahkan reaktan lain?")
        
        if reaksikan and senyawa_1:
            senyawa_2 = st.text_input("Masukkan Nama Senyawa Kedua:")
            if senyawa_2:
                # Cek di database reaksi lokal
                reaktan_set = frozenset([senyawa_1.lower(), senyawa_2.lower()])
                
                if reaktan_set in REACTION_DATABASE:
                    data_reaksi = REACTION_DATABASE[reaktan_set]
                    st.info(f"**Jenis Reaksi:** {data_reaksi['jenis_reaksi']}")
                    st.write(data_reaksi['penjelasan'])
                    
                    produk = get_compound_data(data_reaksi['produk'])
                    if produk:
                        st.success(f"**Produk Hasil Reaksi:** {produk.iupac_name}")
                        st.write(f"- Rumus Molekul Produk: {produk.molecular_formula}")
                        st.write(f"- Berat Molekul Produk: {produk.molecular_weight} g/mol")
                        st.write("**Struktur 3D Produk:**")
                        render_3d_molecule(produk.cid)
                else:
                    st.warning("Reaksi spesifik antara dua senyawa ini belum ada dalam database lokal atau memerlukan kondisi lab tertentu yang kompleks.")

elif menu == "Latihan Soal":
    st.header("🧠 Latihan Soal Tata Nama")
    st.write("Tebak nama IUPAC atau Trivial dari struktur senyawa berikut!")
    
    # Inisialisasi state untuk soal
    if 'current_q' not in st.session_state:
        st.session_state.current_q = random.choice(QUIZ_DATA)
        
    if st.button("Acak Soal Baru"):
        st.session_state.current_q = random.choice(QUIZ_DATA)
        
    soal = st.session_state.current_q
    
    st.write("**Perhatikan struktur 3D berikut (Bisa diputar/zoom):**")
    render_3d_molecule(soal['cid'])
    
    jawaban = st.text_input("Masukkan Nama Senyawa (IUPAC atau Trivial):").lower()
    
    if st.button("Cek Jawaban"):
        if jawaban == soal['nama_iupac'].lower() or jawaban == soal['nama_trivial'].lower():
            st.balloons()
            st.success("Tepat sekali! Itu adalah " + soal['nama_iupac'].title())
        else:
            st.error("Kurang tepat, coba teliti lagi gugus fungsinya atau bentuk rantainya.")
            with st.expander("Lihat Kunci Jawaban"):
                st.write(f"IUPAC: {soal['nama_iupac']}")
                st.write(f"Trivial: {soal['nama_trivial']}")

