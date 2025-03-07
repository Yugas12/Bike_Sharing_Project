import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Path relatif ke dataset
dataset_path = os.path.join(os.getcwd(), "data_terbaru.csv")

# Pastikan file dataset ada sebelum membaca
if os.path.exists(dataset_path):
    # Load dataset
    day_df = pd.read_csv(dataset_path)

    # Konversi kolom tanggal
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])

    # Judul Dashboard
    st.title("Dashboard Analisis Bike Sharing")
    st.markdown("### Visualisasi Data Penyewaan Sepeda")

    # Sidebar untuk filter bulan
    st.sidebar.header("Filter Data")
    selected_month = st.sidebar.selectbox("Pilih Bulan", options=range(1, 13), 
                                          format_func=lambda x: ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", 
                                                                 "Agu", "Sep", "Okt", "Nov", "Des"][x-1])
    filtered_data = day_df[day_df['mnth_x'] == selected_month]

    # Tampilkan data yang difilter
    st.subheader("Data Penyewaan Sepeda untuk Bulan yang Dipilih")
    st.dataframe(filtered_data)

    # Visualisasi 1: Jumlah Peminjaman Sepeda Berdasarkan Musim
    st.subheader("Jumlah Peminjaman Sepeda Berdasarkan Musim")
    byseason_df = day_df.groupby(by="season_x").agg({"cnt_x": "sum"}).reset_index()
    byseason_df.rename(columns={"cnt_x": "sum"}, inplace=True)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x="season_x", y="sum", data=byseason_df.sort_values(by="season_x", ascending=False), ax=ax)
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.set_title("Jumlah Sepeda Berdasarkan Musim", loc="center", fontsize=15)
    ax.tick_params(axis="x", labelsize=12)
    st.pyplot(fig)

    # Visualisasi 2: Total Penyewaan Sepeda per Bulan
    st.subheader("Total Penyewaan Sepeda per Bulan")
    bymonth_df = day_df.groupby(by="mnth_x").agg({"cnt_x": "sum"}).reset_index()
    bymonth_df.rename(columns={"cnt_x": "sum"}, inplace=True)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=bymonth_df["mnth_x"], y=bymonth_df["sum"], palette="Blues", ax=ax)
    for index, row in bymonth_df.iterrows():
        ax.text(row['mnth_x'] - 1, row['sum'], f"{int(row['sum'])}", ha="center", va="bottom", fontsize=10)
    ax.set_xlabel("Bulan")
    ax.set_ylabel(None)
    ax.set_title("Jumlah Peminjaman Sepeda per Bulan", loc="center", fontsize=15)
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"], fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

else:
    st.error(f"Dataset tidak ditemukan! Harap pastikan file 'data_terbaru.csv' ada di folder {os.getcwd()}.")
