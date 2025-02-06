pip install plotly

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Konfigurasi halaman
st.set_page_config(page_title="Analisis Saham Mercury", layout="wide")

# Load semua dataset
@st.cache_data
def load_data():
    daily = pd.read_csv('harga_saham_perhari.csv')
    daily_volume = pd.read_csv('harga_saham_perhari_volume.csv')
    
    # Konversi tanggal
    for df in [daily, daily_volume]:
        df['Date'] = pd.to_datetime(df['Date'])
    
    return daily, daily_volume

daily, daily_volume = load_data()

# Sidebar
st.sidebar.header("Pengaturan Analisis")
analysis_type = st.sidebar.radio("Jenis Analisis", 
                               ['Prediksi Harian', 'Prediksi Dengan Faktor Volume'])

# Fungsi filter tanggal
def date_filter(df):
    min_date = df['Date'].min()
    max_date = df['Date'].max()
    
    start_date = st.sidebar.date_input(
        "Tanggal Mulai", 
        value=min_date,
        min_value=min_date,
        max_value=max_date,
        key=f"start_{analysis_type}"
    )
    
    end_date = st.sidebar.date_input(
        "Tanggal Akhir", 
        value=max_date,
        min_value=min_date,
        max_value=max_date,
        key=f"end_{analysis_type}"
    )
    
    return df[(df['Date'] >= pd.to_datetime(start_date)) & 
             (df['Date'] <= pd.to_datetime(end_date))]

# Konten utama
st.title("Analisis Saham Mercury General Corp Pasca Kebakaran Los Angeles")

if analysis_type == 'Prediksi Harian':
    filtered = date_filter(daily)
    
    # Tab untuk visualisasi harian
    tab1, tab2, tab3 = st.tabs(["Trend Harian", "Dampak Kebakaran", "Evaluasi Model"])
    
    with tab1:
        fig = px.line(filtered, x='Date', y='Close', color='Tipe',
                     title='Prediksi vs Aktual (Harian)',
                     labels={'Close': 'Harga Penutupan', 'Date': 'Tanggal'},
                     color_discrete_map={'Real': 'blue', 'Prediksi': 'red'})
        st.plotly_chart(fig, use_container_width=True)
        
    with tab2:
        col1, col2 = st.columns([3,1])
        with col1:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=filtered['Date'], y=filtered['Close'],
                                    mode='lines', name='Harga'))
            fig.add_vline(x=pd.to_datetime('2025-01-10'), line_dash="dash",
                         line_color="black", name='Tanggal Kebakaran')
            fig.update_layout(title='Dampak Kebakaran pada Harga Harian',
                            xaxis_title='Tanggal', yaxis_title='Harga')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.metric("Harga 1 Minggu Sebelum", "65.25")
            st.metric("Harga 1 Minggu Sesudah", "48.63")
            st.metric("Penurunan (%)", "-25.47%")
    
    with tab3:
        st.subheader("Evaluasi Model SARIMAX Harian")
        col1, col2, col3 = st.columns(3)
        col1.metric("RMSE", "2.79")
        col2.metric("MAE", "1.74")
        col3.metric("R²", "-0.042")
        
elif analysis_type == 'Prediksi Dengan Faktor Volume':
    filtered = date_filter(daily_volume)
    
    # Tab untuk analisis harian + volume
    tab1, tab2 = st.tabs(["Trend Harian", "Perbandingan Model"])
    
    with tab1:
        fig = px.line(filtered, x='Date', y='Close', color='Tipe',
                     title='Prediksi vs Aktual (Harian + Volume)',
                     labels={'Close': 'Harga Penutupan', 'Date': 'Tanggal'},
                     color_discrete_map={'Real': 'blue', 'Prediksi': 'red'})
        st.plotly_chart(fig, use_container_width=True)
        
    with tab2:
        st.subheader("Perbandingan Model dengan dan Tanpa Volume")
        st.write("""
        **Insights:**
        - Model dengan variabel volume menunjukkan akurasi yang lebih tinggi
        - RMSE model dengan volume: 2.02 (vs 2.79 tanpa volume)
        - R² model dengan volume: 0.082 (vs -0.042 tanpa volume)
        """)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("RMSE (Dengan Volume)", "2.02")
        col2.metric("MAE (Dengan Volume)", "1.23")
        col3.metric("R² (Dengan Volume)", "0.082")

# Bagian umum untuk semua analisis
st.sidebar.divider()
st.sidebar.download_button(
    label="Download Semua Data",
    data=pd.concat([daily, daily_volume]).to_csv(index=False),
    file_name='all_data.csv',
    mime='text/csv'
)

# Footer
st.markdown("""
---
**Interpretasi Hasil:**
1. Pola penurunan signifikan pasca kebakaran terlihat jelas pada data harian
2. Model dengan variabel tambahan menunjukkan akurasi lebih tinggi
""")
