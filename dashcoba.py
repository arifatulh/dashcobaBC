# -*- coding: utf-8 -*-
import streamlit as st


# ====== KONFIGURASI DASBOR ======
st.set_page_config(
    page_title="Dashboard Gerakan Buang Sampah Terpilah (GBST)",
    page_icon=":bar_chart:",
    layout="wide"
)
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from babel.numbers import format_currency

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
sns.set(style='whitegrid')


# ================================
# AMBIL DATA DARI GOOGLE SHEETS
# ================================
sheet_url = "https://docs.google.com/spreadsheets/d/1WdN8oE10S0fwmQArsIMa8QOwgRyrPds_iwai2qZNzng/edit?usp=sharing"

# ambil ID file dari link
sheet_id = sheet_url.split("/")[5]

# daftar sheet yang ingin dibaca
sheet_names = ["Timbulan", "Program", "Ketidaksesuaian", "Survei_Online", "Survei_Offline", "CCTV"]

all_df = {}
for sheet in sheet_names:
    try:
        url_csv = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet}"
        df = pd.read_csv(url_csv)
        all_df[sheet] = df
    except Exception as e:
        st.error(f"Gagal load sheet {sheet}: {e}")

# gabungkan survei online + offline
if "Survei_Online" in all_df and "Survei_Offline" in all_df:
    all_df["Survei"] = pd.concat([all_df["Survei_Online"], all_df["Survei_Offline"]], ignore_index=True)

# contoh ambil salah satu sheet
if "Timbulan" in all_df:
    df_timbulan = all_df["Timbulan"]
    st.success("Google Sheets loaded successfully!")
    st.write("Preview Data Timbulan:", df_timbulan.head())
else:
    st.warning("Sheet 'Timbulan' tidak ditemukan.")


# ================================
# SIDEBAR
# ================================
with st.sidebar:
    st.image('BerauCoal.png', use_container_width=True)

    selected_topic = st.multiselect(
        "Select Topic(s)",
        options=["ALL", "Timbulan", "Program", "Ketidaksesuaian", "Survei", "CCTV"],
        default=["ALL"]
    )
# ================================
# TAMPILKAN HASIL
# ================================
if selected_topic:
    st.subheader(f"Preview Data: {selected_topic}")
    for topic in selected_topic:
        if topic in all_df:
            st.dataframe(all_df[topic].head())
        else:
            st.warning(f"Topic '{topic}' tidak ditemukan.")
# ================================
# FILTERING DATA
# ================================
if "ALL" in selected_topic:
    main_df = all_df.copy()  # tampilkan semua data
else:
    # hanya simpan sheet terpilih
    main_df = {name: df for name, df in all_df.items() if name in selected_topic}


# ================================
# HALAMAN UTAMA
# ================================
st.markdown("Hello, Semangat PAGI ! :smile: :wave:")
st.header('Dashboard Gerakan Buang Sampah Terpilah (GBST) :bar_chart:')
st.markdown("---")
