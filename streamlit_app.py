import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import streamlit.components.v1 as components
import math

# Konfigurasi Halaman Web
st.set_page_config(page_title="Penetapan Kadar Fosfat", layout="wide", page_icon="🧪")

st.title("🧪 Aplikasi Penetapan Kadar Fosfat dalam Sampel Pupuk")
st.markdown("**Metode Biru Molibdat - Spektrofotometri UV-Vis**")

# Membuat Tab Navigasi
tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 Visual 3D UV-Vis & Prinsip", 
    "📝 Preparasi & Cara Kerja", 
    "📈 Perhitungan & Kurva", 
    "⚖️ Estimasi Ketidakpastian"
])

# ================= TAB 1: VISUAL 3D & PRINSIP =================
with tab1:
    st.header("Visualisasi 3D Spektrofotometer UV-Vis (Shimadzu UV-1800)")
    st.info("💡 **Tips Interaktif:** Klik dan tahan untuk memutar alat, scroll untuk Zoom In/Out. Gunakan tombol untuk membuka kompartemen atau melihat bagian dalam alat (Tembus Pandang).")
    
    # KODE HTML/JS UNTUK THREE.JS 3D
    html_3d = """
    <!DOCTYPE html>
    <html>
    <head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    <style>
      body { margin: 0; overflow: hidden; background: #e9ecef; font-family: sans-serif;}
      #ui { position: absolute; top: 10px; left: 10px; z-index: 10; background: rgba(255,255,255,0.9); padding: 10px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
      button { padding: 8px 12px; cursor: pointer; margin: 4px; border: none; background: #0b5cad; color: white; border-radius: 4px; font-weight: bold;}
      button:hover { background: #08427b; }
    </style>
    </head>
    <body>
    <div id="ui">
      <div style="margin-bottom: 8px;"><b>Kontrol Instrumen</b></div>
      <button onclick="toggleLid()">Buka/Tutup Kompartemen</button>
      <button onclick="toggleXray()">Mode Tembus Pandang</button>
    </div>
    <script>
      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 100);
      camera.position.set(0, 5, 10);

      const renderer = new THREE.WebGLRenderer({antialias: true, alpha: true});
      renderer.setSize(window.innerWidth, window.innerHeight);
      document.body.appendChild(renderer.domElement);

      const controls = new THREE.OrbitControls(camera, renderer.domElement);
      controls.enableDamping = true;
      
      const light = new THREE.DirectionalLight(0xffffff, 1);
      light.position.set(5, 10, 5);
      scene.add(light);
      scene.add(new THREE.AmbientLight(0x606060));

      const matCasing = new THREE.MeshStandardMaterial({color: 0xeeeeee, transparent: true, opacity: 1, roughness: 0.5});
      const matScreen = new THREE.MeshStandardMaterial({color: 0x111111});
      const matInside = new THREE.MeshStandardMaterial({color: 0x555555});
      const matCuvette = new THREE.MeshStandardMaterial({color: 0x88ccff, transparent: true, opacity: 0.7});

      const group = new THREE.Group();
      scene.add(group);

      // Body Utama (Casing UV-1800)
      const bodyGeo = new THREE.BoxGeometry(6, 2, 4);
      const body = new THREE.Mesh(bodyGeo, matCasing);
      body.position.y = 1;
      group.add(body);

      // Layar/Keypad di kanan
      const screen = new THREE.Mesh(new THREE.BoxGeometry(1.5, 0.6, 1.2), matScreen);
      screen.position.set(1.5, 2.1, 0.5);
      screen.rotation.x = -Math.PI / 16;
      group.add(screen);

      // Ruang sampel (kompartemen)
      const compInside = new THREE.Mesh(new THREE.BoxGeometry(2, 1.5, 2), matInside);
      compInside.position.set(-1.5, 1.25, 0.5);
      group.add(compInside);

      // Dudukan Kuvet
      const holder = new THREE.Mesh(new THREE.BoxGeometry(0.8, 0.5, 1.2), new THREE.MeshStandardMaterial({color: 0x222222}));
      holder.position.set(-1.5, 0.75, 0.5);
      group.add(holder);

      // Kuvet Blanko & Sampel
      const cuvette1 = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.6, 0.2), matCuvette);
      cuvette1.position.set(-1.5, 1.2, 0.2);
      group.add(cuvette1);
      
      const cuvette2 = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.6, 0.2), matCuvette);
      cuvette2.position.set(-1.5, 1.2, 0.8);
      group.add(cuvette2);

      // Berkas Cahaya UV-Vis (Terlihat saat tembus pandang)
      const beamMat = new THREE.MeshBasicMaterial({color: 0xff00ff, transparent: true, opacity: 0.6});
      const beam = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, 4), beamMat);
      beam.rotation.z = Math.PI / 2;
      beam.position.set(-1.5, 1.2, 0.5);
      beam.visible = false;
      group.add(beam);

      // Tutup Kompartemen
      const lidGroup = new THREE.Group();
      lidGroup.position.set(-1.5, 2, -0.5);
      group.add(lidGroup);
      
      const lid = new THREE.Mesh(new THREE.BoxGeometry(2.2, 0.15, 2.2), matCasing);
      lid.position.set(0, 0, 1);
      lidGroup.add(lid);

      let lidOpen = false;
      let targetRotation = 0;
      window.toggleLid = function() {
        lidOpen = !lidOpen;
        targetRotation = lidOpen ? -Math.PI / 2.5 : 0;
      }

      let xrayOn = false;
      window.toggleXray = function() {
        xrayOn = !xrayOn;
        matCasing.opacity = xrayOn ? 0.25 : 1.0;
        matCasing.depthWrite = !xrayOn;
        beam.visible = xrayOn;
      }

      function animate() {
        requestAnimationFrame(animate);
        controls.update();
        lidGroup.rotation.x += (targetRotation - lidGroup.rotation.x) * 0.1;
        renderer.render(scene, camera);
      }
      animate();

      window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
      });
    </script>
    </body>
    </html>
    """
    components.html(html_3d, height=450)
    
    st.subheader("Prinsip Kerja Alat (Metode Biru Molibdat)")
    st.write("""
    Fosfat bereaksi dengan amonium molibdat dalam suasana asam membentuk asam molibdofosfat. Kemudian direduksi dengan asam askorbat (atau pereduksi lain) menjadi kompleks biru molibdenum. 
    Intensitas warna biru yang terbentuk sebanding dengan konsentrasi fosfat dan diukur absorbansinya menggunakan spektrofotometer UV-Vis pada panjang gelombang maksimum (biasanya sekitar 880 nm atau 890 nm).
    """)

# ================= TAB 2: PREPARASI & CARA KERJA =================
with tab2:
    st.header("Cara Kerja Penetapan Fosfat")
    st.markdown("""
    **A. Pembuatan Larutan Kerja Fosfat (Deret Standar)**
    1. Siapkan 7 tabung ulir.
    2. Pipet larutan induk fosfat 2 mg/L masing-masing: 0 mL (blanko), 0,5 mL, 1,0 mL, 1,5 mL, 2,0 mL, 2,5 mL, 3.0 mL.
    3. Tambahkan aquabides hingga tanda tera 10 mL dan kocok hingga homogen.
    4. Konsentrasi akhir jadi: 0; 0,1; 0,2; 0,3; 0,4; 0,5; 0,6 mg/L (ppm).

    **B. Preparasi Sampel Pupuk (Destruksi)**
    1. Haluskan sampel pupuk, timbang 0,1 g masukkan ke beaker glass 100 mL.
    2. Tambahkan 5 mL HNO3(p) lalu panaskan di hotplate 100°C hingga keruh.
    3. Dinginkan, tambahkan 2 mL asam perklorat, lalu naikkan suhu ke 170°C hingga larutan bening.
    4. Dinginkan, pindahkan ke labu takar 100 mL, encerkan dengan aquabides hingga tanda tera.
    5. Pipet 0,5 mL larutan tersebut ke labu takar 100 mL lain, encerkan kembali. *(Faktor Pengenceran total)*

    **C. Pengujian Presisi dan Akurasi (Air / Ekstrak)**
    * **Presisi (Duplo):** Sampel diukur berulang untuk melihat kedekatan antar hasil pengukuran.
    * **Akurasi (Spike):** Penambahan standar (spike) ke dalam sampel untuk mengevaluasi *Recovery* hasil.
    """)

# ================= TAB 3: PERHITUNGAN & KURVA =================
with tab3:
    st.header("1. Input Data Deret Standar")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.write("Masukkan Konsentrasi dan Absorbansi")
        # Default data standar
        default_data = pd.DataFrame({
            "Konsentrasi (mg/L)": [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
            "Absorbansi": [0.002, 0.103, 0.196, 0.293, 0.384, 0.473, 0.570]
        })
        edited_df = st.data_editor(default_data, num_rows="dynamic")
    
    with col2:
        x = edited_df["Konsentrasi (mg/L)"].values.reshape(-1, 1)
        y = edited_df["Absorbansi"].values
        
        if len(x) > 2:
            model = LinearRegression()
            model.fit(x, y)
            r_sq = model.score(x, y)
            intercept = model.intercept_
            slope = model.coef_[0]
            
            st.success(f"**Persamaan Regresi:** y = {slope:.4f}x + {intercept:.4f}")
            st.success(f"**R² (Koefisien Determinasi):** {r_sq:.4f}")
            
            # Plot Kurva
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.scatter(x, y, color='blue', label='Data Standar')
            ax.plot(x, model.predict(x), color='red', linestyle='--', label='Regresi Linear')
            ax.set_xlabel("Konsentrasi (mg/L)")
            ax.set_ylabel("Absorbansi")
            ax.set_title("Kurva Kalibrasi Fosfat")
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)
        else:
            st.warning("Masukkan minimal 3 data untuk membuat kurva regresi.")

    st.divider()
    st.header("2. Perhitungan Kadar Sampel")
    
    c1, c2, c3 = st.columns(3)
    abs_sampel = c1.number_input("Absorbansi Sampel", value=0.250, format="%.3f")
    berat_sampel = c2.number_input("Berat Sampel (gram)", value=0.100, format="%.3f")
    fp_sampel = c3.number_input("Faktor Pengenceran (FP)", value=2000) # 100/0.1 * 100/0.5
    
    if len(x) > 2:
        kons_terukur = (abs_sampel - intercept) / slope
        kadar_mgL = kons_terukur * fp_sampel
        kadar_persen = (kadar_mgL * 0.1) / (berat_sampel * 1000) * 100 # Konversi unit
        
        st.info(f"""
        **Hasil Kalkulasi:**
        * Konsentrasi terukur di alat (x) = **{kons_terukur:.4f} mg/L**
        * Kadar setelah dikalikan FP = **{kadar_mgL:.2f} mg/L**
        """)

# ================= TAB 4: ESTIMASI KETIDAKPASTIAN =================
with tab4:
    st.header("Estimasi Ketidakpastian (GUM Method)")
    st.write("Isi spesifikasi alat gelas untuk menghitung penyumbang ketidakpastian baku.")
    
    st.subheader("1. Ketidakpastian Kurva Kalibrasi ($u_{reg}$)")
    if len(x) > 2:
        # Perhitungan u_regresi analitik
        y_pred = model.predict(x)
        syx = np.sqrt(np.sum((y - y_pred)**2) / (len(x) - 2))
        x_mean = np.mean(x)
        Sxx = np.sum((x - x_mean)**2)
        p = 1 # jumlah ulangan sampel
        n = len(x)
        u_reg = (syx / slope) * np.sqrt((1/p) + (1/n) + ((kons_terukur - x_mean)**2 / Sxx))
        st.write(f"- Konsentrasi Sampel ($C_0$) = {kons_terukur:.4f} mg/L")
        st.write(f"- Standar deviasi residual ($S_{{y/x}}$) = {syx:.4f}")
        st.write(f"- Ketidakpastian Regresi ($u_{{reg}}$) = **{u_reg:.5f} mg/L**")
    else:
        st.warning("Kurva regresi belum terbentuk.")

    st.subheader("2. Ketidakpastian Alat Gelas ($u_{vol}$)")
    c1, c2 = st.columns(2)
    vol_labu = c1.number_input("Volume Labu Takar (mL)", value=100.0)
    tol_labu = c1.number_input("Toleransi Labu Takar (± mL)", value=0.10)
    vol_pipet = c2.number_input("Volume Pipet Volumetri (mL)", value=0.5)
    tol_pipet = c2.number_input("Toleransi Pipet Volum (± mL)", value=0.005)
    
    # Kalkulasi ketidakpastian baku alat gelas
    u_kal_labu = tol_labu / math.sqrt(6) # Distribusi triangular
    u_kal_pipet = tol_pipet / math.sqrt(6)
    
    st.write(f"- Ketidakpastian Labu Takar ($u_{{v\_labu}}$) = **{u_kal_labu:.5f} mL**")
    st.write(f"- Ketidakpastian Pipet ($u_{{v\_pipet}}$) = **{u_kal_pipet:.5f} mL**")
    
    if len(x) > 2 and kons_terukur > 0:
        st.subheader("3. Ketidakpastian Gabungan & Diperluas")
        rel_reg = u_reg / kons_terukur
        rel_labu = u_kal_labu / vol_labu
        rel_pipet = u_kal_pipet / vol_pipet
        
        # Gabungan relatif
        u_gab_rel = math.sqrt(rel_reg**2 + rel_labu**2 + rel_pipet**2)
        u_gab = u_gab_rel * kadar_mgL
        U_expand = u_gab * 2 # k=2 (95% confidence)
        
        st.success(f"**Ketidakpastian Baku Gabungan ($u_c$) = {u_gab:.3f} mg/L**")
        st.error(f"**Hasil Akhir Pelaporan:** Kadar = {kadar_mgL:.2f} ± {U_expand:.2f} mg/L (k=2, 95% CI)")

st.caption("Aplikasi dikembangkan menggunakan Python, Streamlit, dan Three.js")
