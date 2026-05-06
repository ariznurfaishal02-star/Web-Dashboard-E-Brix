import ee
import folium
import streamlit as st
from folium.plugins import Fullscreen

def create_ebrix_map(df):
    m = None
    error_msg = None

    try:
        # 1. AMBIL ASET DARI GEE
        heatmap_ebk = ee.Image("projects/fabled-archive-491907-g3/assets/Heatmap_Brix/peta_01")
        heatmap_ebk = heatmap_ebk.sort('system:index', False).first()
        # 2. AMBIL BOUNDS DARI ASSET
        bounds = heatmap_ebk.geometry().bounds().getInfo()
        coords = bounds['coordinates'][0]
        lats = [c[1] for c in coords]
        lons = [c[0] for c in coords]
        center_lat = (min(lats) + max(lats)) / 2
        center_lon = (min(lons) + max(lons)) / 2

        # 3. PETA DASAR
        m = folium.Map(location=[center_lat, center_lon], zoom_start=14)
        folium.TileLayer(
            tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
            attr="Google Satellite",
            name="Satelit",
            overlay=False,
            control=True
        ).add_to(m)

        # 4. AMBIL GAMBAR STATIS DARI GEE
        thumb_url = heatmap_ebk.getThumbURL({
            'min': 8.8,
            'max': 26,
            'palette': ['#2ecc71', '#f39c12', '#e74c3c'],
            'region': bounds,
            'dimensions': 1024,
            'format': 'png'
        })

        # 5. OVERLAY GAMBAR KE PETA
        folium.raster_layers.ImageOverlay(
            image=thumb_url,
            bounds=[[min(lats), min(lons)], [max(lats), max(lons)]],
            opacity=0.8,
            name="Heatmap EBK",
            show=True
        ).add_to(m)

        # 6. LEGENDA
        legend_html = """
        <div style="position: fixed; bottom: 30px; right: 10px; z-index: 1000;
                    background-color: white; color: black; padding: 10px; border-radius: 8px;
                    border: 1px solid #ccc; font-size: 13px;">
            <b>Tingkat Kemanisan (Brix)</b><br>
            <i style="background:#e74c3c;width:12px;height:12px;display:inline-block;margin-right:5px;"></i> Tinggi (&gt; 19)<br>
            <i style="background:#f39c12;width:12px;height:12px;display:inline-block;margin-right:5px;"></i> Sedang (14 - 18)<br>
            <i style="background:#2ecc71;width:12px;height:12px;display:inline-block;margin-right:5px;"></i> Rendah (&lt; 14)
        </div>
        """
        m.get_root().html.add_child(folium.Element(legend_html))

        # 7. TITIK SAMPEL
        if not df.empty:
            for idx, row in df.iterrows():
                if 'Latitude' in row and 'Longitude' in row:
                    folium.CircleMarker(
                        location=[row['Latitude'], row['Longitude']],
                        radius=4,
                        color='white',
                        weight=1,
                        fill=True,
                        fill_color='white',
                        fill_opacity=0.7,
                        tooltip=f"Blok: {row.get('Kode_Blok', '-')} | Brix: {row.get('Nilai_Brix', 0)}°"
                    ).add_to(m)

        # 8. TOMBOL FULLSCREEN
        Fullscreen(
            position="topleft",
            title="Layar Penuh",
            title_cancel="Keluar Layar Penuh",
            force_separate_button=True
        ).add_to(m)

        folium.LayerControl().add_to(m)

    except Exception as e:
        error_msg = str(e)
        st.error(f"❌ Error: {e}")

    return m, error_msg
