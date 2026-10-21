import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats

# Konfigurasi Halaman
st.set_page_config(page_title="Penetapan Kadar Fosfat", layout="wide", page_icon="🧪")

# Judul Aplikasi
st.title("🧪 Penetapan Kadar Fosfat dalam Sampel Pupuk")
st.markdown("Aplikasi interaktif untuk analisis kadar fosfat menggunakan metode Biru Molibdat (Spektrofotometri UV-Vis).")

# Membuat Tab Navigasi
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔍 Visual 3D UV-Vis", 
    "📝 Cara Kerja & Preparasi", 
    "📈 Kurva Kalibrasi & Kadar", 
    "📊 Estimasi Ketidakpastian",
    "📂 Data Excel"
])

# ================= TAB 1: VISUAL 3D =================
with tab1:
    st.header("Visualisasi 3D Spektrofotometer UV-Vis")
    st.markdown("""
    Anda dapat melakukan **Zoom In/Out** (scroll mouse) dan **Rotasi 360°** (klik dan geser) pada model di bawah ini.
    *(Catatan: Ini adalah model viewer bawaan web. Ganti URL `src` dengan link file `.glb` Shimadzu UV 1800 Anda di GitHub agar menampilkan alat aslinya).*
    """)
    
    # Menggunakan HTML tag <model-viewer> dari Google untuk render 3D
    # Atribut material transparan (opacity) bisa diatur di model aslinya.
    html_3d = """
    <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.1.1/model-viewer.min.js"></script>
    <model-viewer 
        src="https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/SciFiHelmet/glTF/SciFiHelmet.gltf" 
        alt="3D model Spektrofotometer" 
        camera-controls 
        auto-rotate 
        interaction-prompt="auto"
        style="width: 100%; height: 500px; background-color: #e5e5f7; border-radius: 10px;">
    </model-viewer>
    """
    st.components.v1.html(html_3d, height=520)
    
    st.subheader("Prinsip Kerja Alat")
    st.info("""
    **Spektrofotometer Shimadzu UV-1800** bekerja berdasarkan hukum **Lambert-Beer**, di mana absorbansi cahaya monokromatis 
    berbanding lurus dengan konsentrasi spesies penyerap (sampel). Pada analisis fosfat metode biru molibdat, ion ortofosfat 
    bereaksi dengan amonium molibdat membentuk asam molibdofosfat yang kemudian direduksi menjadi kompleks berwarna biru. 
    Intensitas warna biru ini diukur pada panjang gelombang spesifik (biasanya ~880 nm) menggunakan detektor UV-Vis.
    """)

# ================= TAB 2: CARA KERJA =================
with tab2:
    st.header("Cara Kerja Penetapan Fosfat - Metode Biru Molibdat")
    
    st.markdown("### A. Pembuatan Larutan Kerja Fosfat (Deret Standar)")
    st.markdown("""
    1. Siapkan 7 tabung ulir.
    2. Pipet larutan induk fosfat 2 mg/L masing-masing: 0 mL (blanko), 0,5 mL, 1,0 mL, 1,5 mL, 2,0 mL, 2,5 mL, 3.0 mL.
    3. Tambahkan aquabides hingga tanda tera 10 mL.
    4. Kocok hingga homogen.
    5. Konsentrasi akhir jadi: 0; 0,1; 0,2; 0,3; 0,4; 0,5; 0,6 mg/L (ppm).
    """)

    st.markdown("### B. Preparasi Sampel Pupuk (Destruksi)")
    st.markdown("""
    1. Haluskan sampel pupuk, timbang 0,1 g masukkan ke beaker glass 100mL.
    2. Tambahkan 5 mL HNO3(p).
    3. Panaskan di atas hotplate suhu 100°C hingga larutan keruh.
    4. Dinginkan, tambahkan 2 mL asam perklorat.
    5. Naikkan suhu hotplate menjadi 170°C, panaskan hingga larutan bening.
    6. Dinginkan, pindahkan ke labu takar 100 mL.
    7. Encerkan dengan aquabides hingga tanda tera.
    8. Pipet 0,5 mL larutan tersebut ke labu takar 100 mL lain, encerkan kembali.
    """)

    st.markdown("### C. Preparasi Sampel Akurasi (Spike)")
    st.markdown("""
    1. Timbang sampel pupuk 0,1 g.
    2. Tambahkan 8 mL larutan baku fosfat 500 mg/L (ini spike-nya).
    3. Lakukan destruksi sama seperti poin B dari awal sampai akhir.
    """)

    st.markdown("### D. Pengujian Sampel Air")
    st.markdown("""
    **1. Presisi Air (Duplo Ulir):**
    * Pipet 10 mL sampel air yang sudah disaring dan diasamkan sampai pH 3 ke tabung ulir.
    * Tambahkan 1,6 mL larutan prekasi kombinasi (campuran asam).
    * Kocok hingga homogen, diamkan 10 menit hingga muncul warna biru.
    * Baca di Spektrofotometer UV-Vis. Kerjakan duplo.
    
    **2. Akurasi Air (Spike):**
    * Pipet 9 mL sampel air (sudah disaring, pH 3) ke tabung ulir.
    * Tambahkan 1 mL standar fosfat 2 ppm.
    * Tambahkan 1,6 mL larutan prekasi kombinasi.
    * Kocok homogen, diamkan 10 menit hingga biru. Baca di UV-Vis.
    
    **3. Blanko:**
    * Pipet 10 mL aquabides ke tabung ulir.
    * Tambahkan 1,6 mL larutan prekasi kombinasi.
    * Kocok homogen, diamkan 10 menit. Baca di UV-Vis sebagai blanko.
    """)

# ================= TAB 3: KURVA & KADAR =================
with tab3:
    st.header("Kurva Kalibrasi & Perhitungan Kadar")
    st.markdown("Masukkan data absorbansi standar untuk membentuk persamaan garis lurus (y = bx + a).")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Data Deret Standar")
        # Default data
        df_standar = pd.DataFrame({
            "Konsentrasi (mg/L)": [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
            "Absorbansi": [0.000, 0.055, 0.112, 0.165, 0.221, 0.278, 0.330]
        })
        edited_df = st.data_editor(df_standar, num_rows="dynamic", use_container_width=True)
    
    with col2:
        st.subheader("Grafik Kurva Kalibrasi")
        x = edited_df["Konsentrasi (mg/L)"].values
        y = edited_df["Absorbansi"].values
        
        if len(x) > 1 and len(x) == len(y):
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            
            fig = px.scatter(edited_df, x="Konsentrasi (mg/L)", y="Absorbansi", title="Kurva Kalibrasi Fosfat")
            fig.add_trace(go.Scatter(x=x, y=slope*x + intercept, mode='lines', name='Regresi Linear'))
            st.plotly_chart(fig, use_container_width=True)
            
            st.success(f"**Persamaan Garis:** y = {slope:.4f}x + {intercept:.4f}")
            st.success(f"**Linearitas (R²):** {r_value**2:.4f}")
        else:
            st.warning("Masukkan data yang valid untuk memunculkan kurva.")

    st.divider()
    st.subheader("Kalkulator Kadar Sampel")
    abs_sampel = st.number_input("Masukkan Absorbansi Sampel:", value=0.150, format="%.3f")
    berat_sampel = st.number_input("Berat Sampel (g):", value=0.100, format="%.3f")
    fp = st.number_input("Faktor Pengenceran (FP):", value=20000, help="Contoh: 100mL / 0.1g * 100mL / 0.5mL = 20000")
    
    if st.button("Hitung Kadar Fosfat"):
        c_sampel = (abs_sampel - intercept) / slope
        kadar = (c_sampel * fp * 1e-3) # Konversi mg/L menyesuaikan unit
        st.info(f"Konsentrasi sampel terukur (C): **{c_sampel:.4f} mg/L**")
        st.success(f"Estimasi Kadar Fosfat dalam sampel: **{kadar:.2f} %** (atau sesuaikan dengan rumus SNI)")

# ================= TAB 4: KETIDAKPASTIAN =================
with tab4:
    st.header("Estimasi Ketidakpastian Pengukuran")
    st.markdown("Mengambil struktur perhitungan berdasarkan file `Blanko Ketidakpastian fosfat.xlsx`")
    
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Ishikawa_Fishbone_Diagram.svg/1024px-Ishikawa_Fishbone_Diagram.svg.png", 
             caption="Diagram Tulang Ikan (Fishbone) Ketidakpastian (Contoh Representasi)", use_container_width=False, width=600)
    
    st.markdown("""
    **Komponen Utama Ketidakpastian Fosfat:**
    1. **Ketidakpastian Kurva Kalibrasi (U_kurva):** Berasal dari variasi regresi linear (slope, sum of squares).
    2. **Ketidakpastian Penimbangan (U_massa):** Berasal dari spesifikasi neraca analitik, sertifikat kalibrasi, efek buoyansi.
    3. **Ketidakpastian Volume (U_vol):** Dari labu takar (kalibrasi, efek suhu) dan pipet volumetrik.
    4. **Ketidakpastian Presisi Metode (U_rep):** Dihitung dari simpangan baku (RSD) pengukuran duplo/pengulangan.
    """)
    
    st.write("Silakan buka Tab 'Data Excel' untuk melihat detail isian sel dari file Excel ketidakpastian Anda.")

# ================= TAB 5: DATA EXCEL =================
with tab5:
    st.header("Integrasi Berkas Laporan Excel")
    st.markdown("Di sini Anda dapat memuat file referensi **`Kelompok 1(A)_Kadar Fosfat(fix).xlsx`** dan **`Blanko Ketidakpastian fosfat.xlsx`** langsung ke dalam website.")
    
    uploaded_kadar = st.file_uploader("Upload 'Kelompok 1(A)_Kadar Fosfat(fix).xlsx'", type=["xlsx", "xls"])
    if uploaded_kadar is not None:
        st.success("File Kadar Fosfat berhasil diunggah!")
        try:
            df_kadar = pd.read_excel(uploaded_kadar)
            st.dataframe(df_kadar, use_container_width=True)
        except Exception as e:
            st.error(f"Gagal membaca file: {e}")

    st.divider()
    
    uploaded_ketidakpastian = st.file_uploader("Upload 'Blanko Ketidakpastian fosfat.xlsx'", type=["xlsx", "xls"])
    if uploaded_ketidakpastian is not None:
        st.success("File Ketidakpastian berhasil diunggah!")
        try:
            df_unc = pd.read_excel(uploaded_ketidakpastian)
            st.dataframe(df_unc, use_container_width=True)
        except Exception as e:
            st.error(f"Gagal membaca file: {e}")
