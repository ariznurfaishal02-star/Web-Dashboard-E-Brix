import streamlit as st
import plotly.express as px

def render_sidebar(df_raw):
    """Menampilkan logo, menu, dan filter di sidebar"""
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;padding:0 0.5rem 0.5rem;">
        <div style="width:38px;height:38px;background:#00b050;border-radius:10px; display:flex;align-items:center;justify-content:center;">
            <b style="color:white; font-size:18px;">EB</b>
        </div>
        <div>
            <div style="color:#fff;font-size:17px;font-weight:800;">E-BRIX</div>
            <div style="color:rgba(255,255,255,.38);font-size:10px;">Sistem Monitoring Tebu</div>
        </div>
    </div>
    <hr style="margin: 10px 0;">
    """, unsafe_allow_html=True)
    
    menu_pilihan = st.radio("Pilih Menu", options=["🟢 Dashboard Peta", "📊 Analisis Data"], label_visibility="collapsed")
    st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
    st.markdown('<p style="color:rgba(255,255,255,.3);font-size:9px;font-weight:700;">🔎 FILTER DATA</p>', unsafe_allow_html=True)
    
    semua_blok = sorted(df_raw['Kode_Blok'].dropna().unique().tolist()) if 'Kode_Blok' in df_raw.columns else []
    blok_dipilih = st.multiselect("Blok Lahan", options=semua_blok, default=[], key="kunci_blok")
    
    tgl_awal, tgl_akhir = None, None
    if 'Tanggal' in df_raw.columns and not df_raw.empty:
        tgl_min = df_raw['Tanggal'].min().date()
        tgl_max = df_raw['Tanggal'].max().date()
        tgl_awal = st.date_input("Dari Tanggal", value=tgl_min, key="kunci_tgl_awal")
        tgl_akhir = st.date_input("Sampai Tanggal", value=tgl_max, key="kunci_tgl_akhir")
    
    if st.button("✕  Reset Filter", use_container_width=True): 
        for k in ['kunci_blok', 'kunci_tgl_awal', 'kunci_tgl_akhir']:
            if k in st.session_state:
                del st.session_state[k]
        st.rerun()
        
    return menu_pilihan, blok_dipilih, tgl_awal, tgl_akhir

def render_header_and_metrics(df):
    """Menampilkan judul utama dan 4 kotak metrik angka"""
    st.markdown("""
    <div style="display:flex;justify-content:space-between;align-items:center; background:#fff;border-radius:12px;padding:14px 20px; border:1px solid rgba(0,0,0,0.07); margin-bottom:1rem;">
        <div>
            <h2 style="margin:0;font-size:1.05rem;font-weight:800;color:#1a2e20;">Dashboard Monitoring Brix</h2>
            <p style="margin:2px 0 0;font-size:10.5px;color:#7a9a84;">Musim Tanam 2026 &nbsp;·&nbsp; Diperbarui: hari ini</p>
        </div>
        <span style="background:#e6f7ed;color:#1a7a40;font-size:10.5px;font-weight:700; padding:4px 12px;border-radius:20px;">● Sistem Aktif</span>
    </div>
    """, unsafe_allow_html=True)

    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric("Rata-rata Brix", f"{round(df['Nilai_Brix'].mean(), 1) if not df.empty else 0}°")
    col_m2.metric("Blok Ditampilkan", df['Kode_Blok'].nunique() if ('Kode_Blok' in df.columns and not df.empty) else "–")
    col_m3.metric("Brix Tertinggi", f"{round(df['Nilai_Brix'].max(), 1) if not df.empty else 0}°")
    col_m4.metric("Brix Terendah", f"{round(df['Nilai_Brix'].min(), 1) if not df.empty else 0}°")
    st.markdown("<div style='margin-bottom:0.9rem'></div>", unsafe_allow_html=True)

def render_analysis_charts(df):
    """Menampilkan grafik garis dan batang untuk menu Analisis Data"""
    # #aaaaaa = abu-abu netral, untuk di bar chart agar angka tetap terlihat 
    AXIS_COLOR = '#aaaaaa'

    plotly_base = dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=10, b=0),
        height=240,
        font=dict(color=AXIS_COLOR)
    )
    axis_style = dict(
    tickfont=dict(color=AXIS_COLOR),
    title_font=dict(color=AXIS_COLOR),
    gridcolor='rgba(150,150,150,0.15)',
    zerolinecolor='rgba(150,150,150,0.15)'
)
    col_kiri, col_kanan = st.columns(2)
    
    with col_kiri:
        with st.container(border=True):
            st.subheader("📈 Tren Kenaikan Brix")
            if 'Tanggal' in df.columns and not df.empty:
                df_trend = df.groupby('Tanggal')['Nilai_Brix'].mean().reset_index()
                fig_trend = px.line(df_trend, x='Tanggal', y='Nilai_Brix', markers=True, color_discrete_sequence=['#00b050'])
                fig_trend.update_layout(**plotly_base)
                fig_trend.update_xaxes(**axis_style)
                fig_trend.update_yaxes(**axis_style)
                st.plotly_chart(fig_trend, use_container_width=True)
            else:
                st.info("📉 Data tidak tersedia.")
                
    with col_kanan:
        with st.container(border=True):
            st.subheader("📊 Status Blok Lahan")
            if 'Kode_Blok' in df.columns and not df.empty:
                df_status = df.groupby('Kode_Blok')['Nilai_Brix'].mean().reset_index().sort_values('Nilai_Brix', ascending=False)
                fig_bar = px.bar(df_status, x='Kode_Blok', y='Nilai_Brix', color='Nilai_Brix', color_continuous_scale=['#2ecc71', '#f39c12', '#e74c3c'])
                fig_bar.update_layout(**plotly_base, coloraxis_showscale=False)
                fig_bar.update_xaxes(**axis_style)
                fig_bar.update_yaxes(**axis_style)
                st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.info("📊 Data tidak tersedia.")
