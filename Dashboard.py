import streamlit as st
import os
import ee
from streamlit_folium import st_folium

# Import modul terpisah
from data_loader import load_data
from map_generator import create_ebrix_map
import ui_component

# 1. INISIALISASI & CONFIG
try:
    ee.Initialize(project='fabled-archive-491907-g3')
    gee_ready = True
except Exception:
    gee_ready = False

st.set_page_config(page_title="E-BRIX Dashboard", page_icon="🍃", layout="wide")

# CSS Loader
current_dir = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(current_dir, "assets/style.css")) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except Exception:
    st.warning("⚠️ File style.css tidak ada.")

# 2. LOAD DATA
df_raw = load_data()

# 3. SIDEBAR & FILTERING
with st.sidebar:
    menu_pilihan, blok_dipilih, tgl_awal, tgl_akhir = ui_component.render_sidebar(df_raw)

# Terapkan Filter
df = df_raw.copy()
if len(blok_dipilih) > 0: 
    df = df[df['Kode_Blok'].isin(blok_dipilih)]
if tgl_awal and tgl_akhir and not df.empty:
    df = df[(df['Tanggal'].dt.date >= tgl_awal) & (df['Tanggal'].dt.date <= tgl_akhir)]

# 4. TAMPILKAN HEADER METRIK
ui_component.render_header_and_metrics(df)

# 5. KONTEN UTAMA
if menu_pilihan == "🟢 Dashboard Peta":
    with st.container(border=True):
        st.subheader("🗺️ Peta Kemanisan Tebu")
        if df.empty or not gee_ready:
            st.warning("Data tidak tersedia atau GEE belum siap.")
        else:
            map_obj, error_msg = create_ebrix_map(df)
            if error_msg:
                st.error(f"Gagal memuat peta: {error_msg}")
            else:
                st_folium(map_obj, use_container_width=True, height=590, returned_objects=[])

elif menu_pilihan == "📊 Analisis Data":
    ui_component.render_analysis_charts(df)