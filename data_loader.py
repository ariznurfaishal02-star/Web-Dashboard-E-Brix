import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("Data_eBrix_Variatif_Kategori.csv", sep=",", decimal=".")
    except FileNotFoundError:
        # Mengembalikan tabel kosong agar aplikasi tidak mati
        return pd.DataFrame(columns=['Tanggal', 'Kode_Blok', 'Latitude', 'Longitude', 'Nilai_Brix'])
    
    df = df.dropna(subset=['Latitude', 'Longitude', 'Nilai_Brix'])
    if 'Tanggal' in df.columns:
        df['Tanggal'] = pd.to_datetime(df['Tanggal'])
    return df