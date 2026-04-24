import pandas as pd
import streamlit as st
import os

@st.cache_data
def load_data():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, "Data_eBrix_Variatif_Kategori.csv")
        df = pd.read_csv(path, sep=",", decimal=".")
    except FileNotFoundError:
        return pd.DataFrame(columns=['Tanggal', 'Kode_Blok', 'Latitude', 'Longitude', 'Nilai_Brix'])

    df = df.dropna(subset=['Latitude', 'Longitude', 'Nilai_Brix'])
    if 'Tanggal' in df.columns:
        df['Tanggal'] = pd.to_datetime(df['Tanggal'])
    return df
