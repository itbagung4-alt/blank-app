import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import streamlit.components.v1 as components
import math

# ================= KONFIGURASI HALAMAN =================
st.set_page_config(page_title="Penetapan Kadar Fosfat", layout="wide", page_icon="🧪")

st.title("🧪 Aplikasi Penetapan Kadar Fosfat dalam Sampel Pupuk")
st.markdown("**Metode Biru Molibdat - Spektrofotometri UV-Vis**")

# ================= TAB NAVIGASI =================
tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 Visual 3D UV-Vis & Prinsip", 
    "📝 Preparasi & Cara Kerja", 
    "📈 Perhitungan & Kurva", 
    "⚖️ Estimasi Ketidakpastian"
])

# ================= TAB 1: VISUAL 3D & PRINSIP =================
with tab1:
    st.header("Visualisasi 3D Spektrofotometer UV-1800")
    st.info("💡 **Panduan:** Geser untuk memutar alat, scroll untuk Zoom. Gunakan tombol di sudut kiri atas untuk membuka kompartemen, melihat jalur cahaya, dan simulasi tembus pandang.")
    
    # Kode HTML/JS 3D yang sudah diperbarui dan mendetail
    html_3d = """
    <!DOCTYPE html>
    <html lang="id">
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    <style>
      :root { --ac: #0b5cad; --fg: #1b2027; }
      body { margin: 0; overflow: hidden; background: #e9ecef; font-family: "Segoe UI", sans-serif; color: var(--fg); }
      #canvas-container { width: 100vw; height: 100vh; position: absolute; top: 0; left: 0; z-index: 1; }
      #ui-panel {
        position: absolute; top: 15px; left: 15px; z-index: 10;
        background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(8px);
        padding: 15px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); max-width: 300px;
      }
      h2 { margin: 0 0 10px 0; font-size: 16px; color: var(--ac); }
      p.desc { font-size: 12px; color: #555; line-height: 1.4; margin-bottom: 12px; }
      .btn-group { display: flex; flex-direction: column; gap: 8px; }
      button {
        background: #fff; border: 1px solid var(--ac); color: var(--ac);
        padding: 8px; border-radius: 6px; font-weight: bold; cursor: pointer;
        transition: all 0.2s; text-align: left; font-size: 12px;
      }
      button:hover { background: var(--ac); color: #fff; }
      button.active { background: var(--ac); color: #fff; box-shadow: inset 0 2px 4px rgba(0,0,0,0.2); }
      
      #prep-panel {
        position: absolute; top: 15px; right: 15px; z-index: 10;
        background: rgba(255, 255, 255, 0.9); padding: 15px;
        border-radius: 12px; width: 260px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        display: none; max-height: 80vh; overflow-y: auto;
      }
      .step { border-left: 3px solid var(--ac); padding-left: 10px; margin-bottom: 10px; font-size: 12px; }
      .step b { display: block; color: var(--fg); margin-bottom: 3px; }
    </style>
    </head>
    <body>
    <div id="ui-panel">
      <h2>Shimadzu UV-1800</h2>
      <p class="desc">Spektrofotometer UV-Vis Sinar Ganda (Double Beam).</p>
      <div class="btn-group">
        <button id="btn-lid" onclick="toggleLid()">Buka Kompartemen Sampel</button>
        <button id="btn-xray" onclick="toggleXray()">Mode Tembus Pandang</button>
        <button id="btn-beam" onclick="toggleBeam()">Jalur Cahaya (Prinsip Kerja)</button>
        <button id="btn-prep" onclick="togglePrep()">Ringkasan Preparasi</button>
      </div>
    </div>

    <div id="prep-panel">
      <h2>Preparasi Fosfat</h2>
      <div class="step"><b>1. Penimbangan</b>0,1 g sampel pupuk.</div>
      <div class="step"><b>2. Destruksi Tahap 1</b>5 mL HNO3(p), panaskan 100°C.</div>
      <div class="step"><b>3. Destruksi Tahap 2</b>2 mL HClO4, panaskan 170°C.</div>
      <div class="step"><b>4. Pelarutan</b>Tera 100 mL dengan aquabides.</div>
      <div class="step"><b>5. Pengukuran</b>Tambah pereaksi, baca absorbansi.</div>
    </div>

    <div id="canvas-container"></div>
    <script>
      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(40, window.innerWidth / window.innerHeight, 0.1, 100);
      camera.position.set(0, 8, 14);
      const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
      renderer.setSize(window.innerWidth, window.innerHeight);
      document.getElementById('canvas-container').appendChild(renderer.domElement);
      const controls = new THREE.OrbitControls(camera, renderer.domElement);
      controls.enableDamping = true; controls.maxPolarAngle = Math.PI / 2 - 0.05;

      scene.add(new THREE.AmbientLight(0xffffff, 0.6));
      const dirLight = new THREE.DirectionalLight(0xffffff, 0.5);
      dirLight.position.set(10, 15, 10); scene.add(dirLight);

      const matBody = new THREE.MeshStandardMaterial({ color: 0xeaeaea, roughness: 0.7 });
      const matDarkPanel = new THREE.MeshStandardMaterial({ color: 0x333538, roughness: 0.6 });
      const matLid = new THREE.MeshStandardMaterial({ color: 0x4a4f55, roughness: 0.5 });
      const matScreen = new THREE.MeshStandardMaterial({ color: 0x8fbc8f, emissive: 0x224422 });
      const matInside = new THREE.MeshStandardMaterial({ color: 0x222222 });

      const uv1800 = new THREE.Group(); scene.add(uv1800);

      const base = new THREE.Mesh(new THREE.BoxGeometry(8, 2, 5), matBody);
      base.position.y = 1; uv1800.add(base);

      const rightPanel = new THREE.Mesh(new THREE.BoxGeometry(3.9, 0.8, 4.8), matDarkPanel);
      rightPanel.position.set(2, 2.4, 0);
      const screen = new THREE.Mesh(new THREE.PlaneGeometry(2.2, 1.2), matScreen);
      screen.rotation.x = -Math.PI / 2; screen.position.set(0, 0.41, -0.5);
      rightPanel.add(screen); uv1800.add(rightPanel);

      const compartment = new THREE.Mesh(new THREE.BoxGeometry(3.8, 1.8, 4.8), matInside);
      compartment.position.set(-1.95, 1.9, 0); uv1800.add(compartment);

      const holder = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.8, 2), new THREE.MeshStandardMaterial({ color: 0x111111 }));
      holder.position.set(-1.95, 1.4, 0.5); uv1800.add(holder);

      const matCuvette = new THREE.MeshPhysicalMaterial({ color: 0xaaddff, transparent: true, opacity: 0.6 });
      const cuv1 = new THREE.Mesh(new THREE.BoxGeometry(0.3, 1, 0.3), matCuvette); cuv1.position.set(-1.95, 2.2, 1); 
      const cuv2 = new THREE.Mesh(new THREE.BoxGeometry(0.3, 1, 0.3), matCuvette); cuv2.position.set(-1.95, 2.2, 0); 
      uv1800.add(cuv1); uv1800.add(cuv2);

      const lidGroup = new THREE.Group(); lidGroup.position.set(-1.95, 2.8, -2.4); uv1800.add(lidGroup);
      const lid = new THREE.Mesh(new THREE.BoxGeometry(3.9, 0.1, 4.8), matLid); lid.position.set(0, 0, 2.4); lidGroup.add(lid);

      const beamGroup = new THREE.Group(); beamGroup.visible = false; uv1800.add(beamGroup);
      const lamp = new THREE.Mesh(new THREE.SphereGeometry(0.3, 16, 16), new THREE.MeshBasicMaterial({ color: 0xffffaa })); lamp.position.set(-3.2, 2.2, -1.5); beamGroup.add(lamp);
      const prism = new THREE.Mesh(new THREE.CylinderGeometry(0, 0.4, 0.6, 3), new THREE.MeshStandardMaterial({ color: 0xaaaaaa })); prism.rotation.x = Math.PI / 2; prism.position.set(-1.95, 2.2, -1.5); beamGroup.add(prism);
      const beamIn = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 1.2), new THREE.MeshBasicMaterial({ color: 0xffffee, transparent: true, opacity: 0.7 })); beamIn.rotation.z = Math.PI / 2; beamIn.position.set(-2.6, 2.2, -1.5); beamGroup.add(beamIn);
      const beamOut = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 2.5), new THREE.MeshBasicMaterial({ color: 0xff3333, transparent: true, opacity: 0.7 })); beamOut.rotation.x = Math.PI / 2; beamOut.position.set(-1.95, 2.2, -0.25); beamGroup.add(beamOut);
      const beamTrans = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 1.5), new THREE.MeshBasicMaterial({ color: 0xff3333, transparent: true, opacity: 0.3 })); beamTrans.rotation.x = Math.PI / 2; beamTrans.position.set(-1.95, 2.2, 1.5); beamGroup.add(beamTrans);
      const detector = new THREE.Mesh(new THREE.BoxGeometry(0.8, 0.8, 0.4), new THREE.MeshStandardMaterial({ color: 0x8b0000 })); detector.position.set(-1.95, 2.2, 2.3); beamGroup.add(detector);

      let isLidOpen = false, targetLidAngle = 0, isXray = false, isBeamOn = false;
      const originalMaterials = [base, rightPanel, lid].map(m => m.material.clone());

      window.toggleLid = () => { isLidOpen = !isLidOpen; targetLidAngle = isLidOpen ? -Math.PI / 2.5 : 0; document.getElementById('btn-lid').classList.toggle('active'); }
      window.toggleXray = () => {
        isXray = !isXray; document.getElementById('btn-xray').classList.toggle('active');
        [base, rightPanel, lid].forEach((mesh, index) => {
          mesh.material = isXray ? new THREE.MeshStandardMaterial({ color: originalMaterials[index].color, transparent: true, opacity: 0.15, depthWrite: false }) : originalMaterials[index];
        });
      }
      window.toggleBeam = () => { isBeamOn = !isBeamOn; beamGroup.visible = isBeamOn; document.getElementById('btn-beam').classList.toggle('active'); if(isBeamOn && !isXray && !isLidOpen) toggleXray(); }
      window.togglePrep = () => { const p = document.getElementById('prep-panel'); p.style.display = p.style.display === 'block' ? 'none' : 'block'; document.getElementById('btn-prep').classList.toggle('active'); }

      let time = 0;
      function animate() {
        requestAnimationFrame(animate); controls.update();
        lidGroup.rotation.x += (targetLidAngle - lidGroup.rotation.x) * 0.1;
        if(isBeamOn) { time += 0.1; lamp.material.color.setHSL(0.15, 1, 0.5 + Math.sin(time*2)*0.1); screen.material.emissiveIntensity = 0.5 + Math.sin(time)*0.2; }
        renderer.render(scene, camera);
      }
      animate();
      window.addEventListener('resize', () => { camera.aspect = window.innerWidth / window.innerHeight; camera.updateProjectionMatrix(); renderer.setSize(window.innerWidth, window.innerHeight); });
    </script>
    </body>
    </html>
    """
    components.html(html_3d, height=550)

# ================= TAB 2: PREPARASI & CARA KERJA =================
with tab2:
    st.header("Cara Kerja Penetapan Fosfat")
    st.markdown("""
    ### A. Pembuatan Larutan Kerja Fosfat (Deret Standar)
    1. Siapkan 7 tabung ulir.
    2. Pipet larutan induk fosfat 2 mg/L masing-masing: **0 mL (blanko), 0,5 mL, 1,0 mL, 1,5 mL, 2,0 mL, 2,5 mL, 3.0 mL**.
    3. Tambahkan aquabides hingga tanda tera 10 mL dan kocok hingga homogen.
    4. Konsentrasi akhir jadi: **0; 0,1; 0,2; 0,3; 0,4; 0,5; 0,6 mg/L (ppm)**.

    ### B. Preparasi Sampel Pupuk (Destruksi)
    1. Haluskan sampel pupuk, timbang **0,1 g** masukkan ke beaker glass 100 mL.
    2. Tambahkan **5 mL HNO3(p)** lalu panaskan di hotplate 100°C hingga keruh.
    3. Dinginkan, tambahkan **2 mL Asam Perklorat**, lalu naikkan suhu ke 170°C hingga larutan bening.
    4. Dinginkan, pindahkan ke labu takar **100 mL**, encerkan dengan aquabides hingga tanda tera.
    5. Pipet **0,5 mL** larutan tersebut ke labu takar **100 mL** lain, encerkan kembali. *(FP Total = 20.000)*

    ### C. Pengujian Presisi dan Akurasi (Air / Ekstrak)
    * **Presisi (Duplo):** Pipet sampel ke tabung ulir + larutan prekasi kombinasi, diamkan 10 menit (biru), baca di UV-Vis (duplo).
    * **Akurasi (Spike):** Timbang sampel 0,1 g + 8 mL baku fosfat 500 mg/L, lakukan proses destruksi yang sama untuk mengevaluasi *Recovery*.
    """)

# ================= TAB 3: PERHITUNGAN & KURVA =================
with tab3:
    st.header("1. Input Data Deret Standar")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.write("Masukkan Konsentrasi dan Absorbansi")
        default_data = pd.DataFrame({
            "Konsentrasi (mg/L)": [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
            "Absorbansi": [0.002, 0.103, 0.196, 0.293, 0.384, 0.473, 0.570]
        })
        edited_df = st.data_editor(default_data, num_rows="dynamic")
    
    with col2:
        x = edited_df["Konsentrasi (mg/L)"].dropna().values.reshape(-1, 1)
        y = edited_df["Absorbansi"].dropna().values
        
        if len(x) > 2:
            model = LinearRegression()
            model.fit(x, y)
            r_sq = model.score(x, y)
            intercept = model.intercept_
            slope = model.coef_[0]
            
            st.success(f"**Persamaan Regresi:** y = {slope:.4f}x + {intercept:.4f}")
            st.success(f"**R² (Koefisien Determinasi):** {r_sq:.4f}")
            
            fig, ax = plt.subplots(figsize=(6, 3.5))
            ax.scatter(x, y, color='blue', label='Data Standar')
            ax.plot(x, model.predict(x), color='red', linestyle='--', label='Regresi Linear')
            ax.set_xlabel("Konsentrasi (mg/L)")
            ax.set_ylabel("Absorbansi")
            ax.set_title("Kurva Kalibrasi Fosfat")
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)

    st.divider()
    st.header("2. Perhitungan Kadar Sampel")
    
    c1, c2, c3 = st.columns(3)
    abs_sampel = c1.number_input("Absorbansi Sampel", value=0.250, format="%.3f")
    berat_sampel = c2.number_input("Berat Sampel (gram)", value=0.100, format="%.3f")
    fp_sampel = c3.number_input("Faktor Pengenceran (FP)", value=20000)
    
    if len(x) > 2:
        kons_terukur = (abs_sampel - intercept) / slope
        kadar_mgL = kons_terukur * fp_sampel
        kadar_persen = (kadar_mgL * 0.1) / (berat_sampel * 1000) * 100
        
        st.info(f"""
        **Hasil Kalkulasi:**
        * Konsentrasi terukur di alat (x) = **{kons_terukur:.4f} mg/L**
        * Kadar Fosfat setelah FP = **{kadar_mgL:,.2f} mg/L**
        * Persentase Kadar = **{kadar_persen:.2f} %**
        """)

# ================= TAB 4: ESTIMASI KETIDAKPASTIAN =================
with tab4:
    st.header("Estimasi Ketidakpastian (GUM Method)")
    
    if len(x) > 2:
        y_pred = model.predict(x)
        syx = np.sqrt(np.sum((y - y_pred)**2) / (len(x) - 2))
        x_mean = np.mean(x)
        Sxx = np.sum((x - x_mean)**2)
        p = 1
        n = len(x)
        
        u_reg = (syx / slope) * np.sqrt((1/p) + (1/n) + ((kons_terukur - x_mean)**2 / Sxx))
        
        st.subheader("1. Ketidakpastian Kurva Kalibrasi ($u_{reg}$)")
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
    
    u_kal_labu = tol_labu / math.sqrt(6) 
    u_kal_pipet = tol_pipet / math.sqrt(6)
    
    st.write(f"- Ketidakpastian Labu Takar ($u_{{v\_labu}}$) = **{u_kal_labu:.5f} mL**")
    st.write(f"- Ketidakpastian Pipet ($u_{{v\_pipet}}$) = **{u_kal_pipet:.5f} mL**")
    
    if len(x) > 2 and kons_terukur > 0:
        st.subheader("3. Ketidakpastian Gabungan & Pelaporan")
        rel_reg = u_reg / kons_terukur
        rel_labu = u_kal_labu / vol_labu
        rel_pipet = u_kal_pipet / vol_pipet
        
        u_gab_rel = math.sqrt(rel_reg**2 + rel_labu**2 + rel_pipet**2)
        u_gab = u_gab_rel * kadar_mgL
        U_expand = u_gab * 2
        
        st.success(f"**Ketidakpastian Baku Gabungan ($u_c$) = {u_gab:.3f} mg/L**")
        st.error(f"**Hasil Akhir Pelaporan:** Kadar Fosfat = {kadar_mgL:,.2f} ± {U_expand:,.2f} mg/L (k=2, 95% Tingkat Kepercayaan)")
