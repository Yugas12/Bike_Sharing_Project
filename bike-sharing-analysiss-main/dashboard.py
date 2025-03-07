import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Judul Dashboard
st.title("Dashboard Analisis Bike Sharing")
st.markdown("### Visualisasi Data Penyewaan Sepeda")

# Pastikan path dataset sesuai dengan struktur repo di GitHub
dataset_path = os.path.join(os.path.dirname(__file__), "bike-sharing-analysiss-main")
csv_file = os.path.join(dataset_path, "data_terbaru.csv")

# Cek apakah file tersedia
if os.path.exists(csv_file):
    day_df = pd.read_csv(csv_file)
else:
    # Opsi upload manual jika file tidak ditemukan
    st.warning("File data_terbaru.csv tidak ditemukan. Silakan upload file CSV secara manual.")
    uploaded_file = st.file_uploader("Upload data CSV", type="csv")
    
    if uploaded_file:
        day_df = pd.read_csv(uploaded_file)
        st.success("File berhasil diunggah!")
    else:
        st.stop()

# Konversi kolom tanggal
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Sidebar untuk filter bulan
st.sidebar.header("Filter Data")
selected_month = st.sidebar.selectbox(
    "Pilih Bulan",
    options=range(1, 13),
    format_func=lambda x: ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"][x-1]
)
filtered_data = day_df[day_df['mnth_x'] == selected_month]

# Tampilkan data yang difilter
st.subheader("Data Penyewaan Sepeda untuk Bulan yang Dipilih")
st.dataframe(filtered_data)

# Visualisasi 1: Jumlah Peminjaman Sepeda Berdasarkan Musim
st.subheader("Jumlah Peminjaman Sepeda Berdasarkan Musim")

# Mapping angka season_x ke nama musim
season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
byseason_df = day_df.groupby(by="season_x").agg({"cnt_x": "sum"}).reset_index()
byseason_df.rename(columns={"cnt_x": "sum"}, inplace=True)
byseason_df["season_x"] = byseason_df["season_x"].replace(season_mapping)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x="season_x", y="sum", data=byseason_df, ax=ax)
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
