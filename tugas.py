import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

st.set_page_config(page_title="Dashboard Temperatur Bandung", layout="wide")

st.title("🌡️ Dashboard Temperatur Kota Bandung")
st.markdown("Upload file CSV berisi data temperatur harian.")

uploaded_file = st.file_uploader("Pilih file CSV", type=["csv"])

if uploaded_file:
    # Baca file dengan delimiter ';'
    df = pd.read_csv(uploaded_file, delimiter=';')
    
    # Gabungkan kolom tanggal
    df['tanggal'] = pd.to_datetime(df[['YEAR', 'MO', 'DY', 'HR']].rename(
        columns={'YEAR': 'year', 'MO': 'month', 'DY': 'day', 'HR': 'hour'}
    ))
    df['suhu'] = df['T2M']
    
    # Tidak perlu filter kota
    if df.empty:
        st.warning("Data kosong.")
    else:
        st.success("Data berhasil dimuat!")
        st.dataframe(df.head(), use_container_width=True)

        # Tambahan kolom bulan dan tahun
        df['bulan'] = df['tanggal'].dt.month
        df['tahun'] = df['tanggal'].dt.year
        df['bulan_tahun'] = df['tanggal'].dt.to_period('M')

        st.subheader("📈 1. Tren Temperatur Harian")
        fig1, ax1 = plt.subplots(figsize=(10, 4))
        ax1.plot(df['tanggal'], df['suhu'], color='tomato')
        ax1.set_xlabel("Tanggal")
        ax1.set_ylabel("Suhu (°C)")
        ax1.set_title("Temperatur Harian di Bandung")
        st.pyplot(fig1)

        st.subheader("📊 2. Rata-rata Suhu Bulanan")
        monthly_avg = df.groupby('bulan_tahun')['suhu'].mean()
        fig2, ax2 = plt.subplots(figsize=(10, 4))
        monthly_avg.plot(kind='bar', color='skyblue', ax=ax2)
        ax2.set_ylabel("Rata-rata Suhu (°C)")
        ax2.set_title("Rata-rata Suhu Bulanan")
        st.pyplot(fig2)

        st.subheader("📉 3. Distribusi Suhu")
        fig3, ax3 = plt.subplots()
        sns.histplot(df['suhu'], bins=20, kde=True, ax=ax3, color='green')
        ax3.set_title("Distribusi Suhu di Bandung")
        ax3.set_xlabel("Suhu (°C)")
        st.pyplot(fig3)

        st.subheader("🌡️ 4. Heatmap Suhu Harian")
        pivot_table = df.pivot_table(index=df['tanggal'].dt.month,
                                     columns=df['tanggal'].dt.day,
                                     values='suhu')
        fig4, ax4 = plt.subplots(figsize=(12, 5))
        sns.heatmap(pivot_table, cmap='coolwarm', ax=ax4)
        ax4.set_title("Heatmap Suhu Harian per Bulan")
        ax4.set_xlabel("Hari")
        ax4.set_ylabel("Bulan")
        st.pyplot(fig4)

        st.subheader("📦 5. Boxplot Variasi Suhu per Bulan")
        fig5, ax5 = plt.subplots(figsize=(10, 4))
        sns.boxplot(x='bulan', y='suhu', data=df, palette='Set2', ax=ax5)
        ax5.set_title("Variasi Suhu Bulanan")
        ax5.set_xlabel("Bulan")
        ax5.set_ylabel("Suhu (°C)")
        st.pyplot(fig5)

else:
    st.info("Silakan upload file CSV terlebih dahulu.")

