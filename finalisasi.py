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
        
        # Tambahan informasi di bawah visualisasi
        st.markdown("""
        **Analisis Tren:**
        - Sebelum kebakaran, harga saham relatif stabil di sekitar **65.25 USD**.
        - Setelah kebakaran terjadi pada **10 Januari 2025**, harga turun tajam hingga **48.63 USD**, mengalami penurunan sekitar **25.47%**.
        - Pemulihan harga saham masih belum terlihat dalam data historis yang ada.
        - Investor tampaknya merespons negatif terhadap kejadian ini, mencerminkan sentimen pasar yang pesimis.
        """)
    
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
        
        # Tambahan informasi di bawah visualisasi
        st.markdown("""
        **Analisis Tren dengan Volume:**
        - Volume transaksi meningkat signifikan setelah kebakaran, mengindikasikan aksi jual besar-besaran.
        - Harga saham tetap mengalami penurunan meskipun volume tinggi, menunjukkan dominasi tekanan jual.
        - Model dengan volume menunjukkan akurasi lebih baik karena mempertimbangkan faktor reaksi pasar yang lebih kompleks.
        """)

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
1. Pola penurunan signifikan pasca kebakaran terlihat jelas pada data harian.
2. Model dengan variabel tambahan (volume) menunjukkan akurasi lebih tinggi.
""")
