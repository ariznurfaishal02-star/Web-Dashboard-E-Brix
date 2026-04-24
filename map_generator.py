import ee
import folium

def create_ebrix_map(df):
    m = None
    error_msg = None
    try:
        # 1. PETA DASAR
        m = folium.Map(location=[-7.3, 108.2], zoom_start=15)
        folium.TileLayer(
            tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
            attr="Google Satellite",
            name="Satelit",
            overlay=False,
            control=True
        ).add_to(m)

        # 2. AMBIL ASET DARI GEE
        heatmap_ebk = ee.Image("projects/fabled-archive-491907-g3/assets/Heatmap_brix_variasi")

        # 3. VISUALISASI
        brix_vis = {
            'min': 8.8,
            'max': 26,
            'palette': ['#2ecc71', '#f39c12', '#e74c3c']
        }

        # 4. TILE URL DARI GEE
        map_id = heatmap_ebk.getMapId(brix_vis)
        tile_url = map_id['tile_fetcher'].url_format

        folium.TileLayer(
            tiles=tile_url,
            attr="Google Earth Engine",
            name="Heatmap EBK",
            overlay=True,
            control=True,
            opacity=0.8,
            show=True
        ).add_to(m)

        # 5. LEGENDA
        legend_html = """
        <div style="position: fixed; bottom: 30px; right: 10px; z-index: 1000;
                    background-color: white; padding: 10px; border-radius: 8px;
                    border: 1px solid #ccc; font-size: 13px;">
            <b>Tingkat Kemanisan (Brix)</b><br>
            <i style="background:#e74c3c;width:12px;height:12px;display:inline-block;margin-right:5px;"></i> Tinggi (&gt; 19)<br>
            <i style="background:#f39c12;width:12px;height:12px;display:inline-block;margin-right:5px;"></i> Sedang (14 - 18)<br>
            <i style="background:#2ecc71;width:12px;height:12px;display:inline-block;margin-right:5px;"></i> Rendah (&lt; 14)
        </div>
        """
        m.get_root().html.add_child(folium.Element(legend_html))

        # 6. TITIK SAMPEL
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

        folium.LayerControl().add_to(m)

    except Exception as e:
        error_msg = str(e)

    return m, error_msg
