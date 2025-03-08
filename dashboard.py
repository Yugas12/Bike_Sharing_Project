import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

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
                                      format_func=lambda x: ["Januari", "Februari", "Maret", "April", "Mei", "Juni", 
                                                             "Juli", "Agustus", "September", "Oktober", "November", "Desember"][x-1])
    filtered_data = day_df[day_df['mnth_x'] == selected_month]

    # Tampilkan data yang difilter
    st.subheader("Data Penyewaan Sepeda untuk Bulan yang Dipilih")
    st.dataframe(filtered_data)

    # Visualisasi 1: Jumlah Peminjaman Sepeda Berdasarkan Musim
    byseason_df = day_df.groupby(by="season_x").agg({"cnt_x": "sum"}).reset_index()
    byseason_df.rename(columns={"cnt_x": "sum", "season_x": "season"}, inplace=True)
    season_labels = {1: "Winter", 2: "Spring", 3: "Summer", 4: "Fall"}
    byseason_df["season"] = byseason_df["season"].map(season_labels)
    max_value = byseason_df["sum"].max()  
    byseason_df["sum"] = byseason_df["sum"] / max_value 
    st.subheader("Jumlah Peminjaman Sepeda Berdasarkan Musim")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(
        y="sum",
        x=byseason_df["season"],  
        data=byseason_df.sort_values(by="season", ascending=False),
        color='steelblue',  # Menggunakan warna biru
        ax=ax
    )
    ax.set_title("Jumlah Sepeda Berdasarkan Musim", loc="center", fontsize=15)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis="x", labelsize=12)
    ax.set_yticks(np.arange(0, 1.2, 0.2))
    ax.set_ylim(0, 1.0)  
    ax.ticklabel_format(style="plain", axis="y")
    st.pyplot(fig)

    # Visualisasi 2: Total Penyewaan Sepeda per Bulan
    data = {
        'mnth': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        'sum': [134933, 151352, 228920, 269094, 331686, 346342, 
                344948, 351194, 345991, 322352, 254831, 211036]
    }
    bymonth_df = pd.DataFrame(data)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(y="sum", x="mnth", data=bymonth_df.sort_values(by="mnth", ascending=True), color='steelblue', ax=ax)

    for index, row in bymonth_df.iterrows():
        ax.text(row['mnth'] - 1, row['sum'], f"{int(row['sum'])}", ha="center", va="bottom", fontsize=10)
    ax.set_title("Jumlah Peminjaman Sepeda per Bulan", loc="center", fontsize=15)
    ax.set_ylabel(None)
    ax.set_xlabel("Month", fontsize=12)
    ax.tick_params(axis="x", labelsize=12)
    st.pyplot(fig)

else:
    st.error(f"Dataset tidak ditemukan! Harap pastikan file 'data_terbaru.csv' ada di folder {os.getcwd()}.")

