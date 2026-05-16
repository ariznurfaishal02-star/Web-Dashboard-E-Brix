import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import os

# 1. Masukkan file CSV 
csv_path = "Data_eBrix_Tren_Naik.csv" 

if os.path.exists(csv_path):
    df_csv = pd.read_csv(csv_path)

    # Ubah baris data jadi titik koordinat (Points)
    geometry = [Point(xy) for xy in zip(df_csv['Longitude'], df_csv['Latitude'])]
    gdf_points = gpd.GeoDataFrame(df_csv, geometry=geometry, crs="EPSG:4326")

    # Bikin garis pembungkus (polygon) otomatis untuk tiap Kode_Blok
    gdf_blok = gdf_points.groupby('Kode_Blok')['geometry'].apply(lambda x: x.unary_union.convex_hull).reset_index()
    gdf_blok = gpd.GeoDataFrame(gdf_blok, geometry='geometry', crs="EPSG:4326")

    # Buat folder khusus agar file Shapefile-nya rapi (tidak berceceran)
    folder_output = "Batas_Blok_SHP"
    if not os.path.exists(folder_output):
        os.makedirs(folder_output)

    # Simpan jadi Shapefile
    gdf_blok.to_file(f"{folder_output}/Batas_Blok_Ebrix.shp", driver="ESRI Shapefile")
    print(f"Shapefile berhasil dibuat di dalam folder '{folder_output}'.")
else:
    print(f"❌ File {csv_path} tidak ditemukan. Cek lagi nama filenya ya.")
