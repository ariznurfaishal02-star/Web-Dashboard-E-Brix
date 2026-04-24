import ee
import geemap.foliumap as geemap
import folium

def create_ebrix_map(df):
    """
    Menghasilkan objek peta Folium yang berisi citra satelit dan 
    overlay heatmap EBK dari Google Earth Engine.
    """
    m = None
    error_msg = None
    
    try:
        # 1. BUAT PETA DASAR
        # Menggunakan geemap agar kompatibel dengan GEE
        m = geemap.Map()
        m.setOptions('SATELLITE') # Tampilan satelit

        # 2. PANGGIL ASET DARI GEE
        # Pastikan Asset ID ini sama persis dengan yang ada di GEE kamu
        heatmap_ebk = ee.Image("projects/fabled-archive-491907-g3/assets/Heatmap_brix_variasi")

        # 3. PENGATURAN VISUALISASI GRADASI WARNA
        brix_vis = {
            'min': 8.8,
            'max': 26,
            'palette': ['#2ecc71', '#f39c12', '#e74c3c'] # Hijau -> Oranye -> Merah
        }

        # 4. TAMBAHKAN LAYER KE PETA
        # Pusatkan kamera ke lokasi heatmap dengan zoom level 15
        m.centerObject(heatmap_ebk, 15)
        
        # Tempelkan gambar heatmap di atas peta satelit
        m.addLayer(heatmap_ebk, brix_vis, 'Heatmap EBK (ArcGIS)')

        # 5. TAMBAHKAN LEGENDA
        # geemap memiliki fungsi bawaan untuk membuat legenda interaktif
        legend_dict = {
            'Tinggi (> 19)': '#e74c3c',
            'Sedang (14 - 18)': '#f39c12',
            'Rendah (< 14)': '#2ecc71'
        }
        m.add_legend(title="Tingkat Kemanisan (Brix)", legend_dict=legend_dict, position='bottomright')

        # 6. TAMBAHKAN TITIK SAMPEL (Opsional)
        # Jika df tidak kosong, tampilkan juga titik-titik sampel aslinya di atas heatmap
        if not df.empty:
            for idx, row in df.iterrows():
                # Pastikan nama kolom 'Latitude' dan 'Longitude' sesuai dengan CSV/Database kamu
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

    except Exception as e:
        # Jika terjadi error saat memanggil GEE, tangkap pesan errornya
        error_msg = str(e)

    # Kembalikan objek peta dan status error ke dashboard.py
    return m, error_msg