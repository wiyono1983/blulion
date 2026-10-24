import streamlit as st
import pandas as pd
import os

FILE_EXCEL = "data_barang.xlsx"

st.title("📦 Data Barang")

if not os.path.exists(FILE_EXCEL):
    pd.DataFrame(columns=["Nama Barang", "Modal"]).to_excel(
        FILE_EXCEL,
        index=False
    )

with st.form("barang"):
    nama_barang = st.text_input("Nama Barang")
    modal = st.number_input("Harga Modal", min_value=0)

    submit = st.form_submit_button("Simpan")

if submit:
    df = pd.read_excel(FILE_EXCEL)

    data_baru = pd.DataFrame([
        {
            "Nama Barang": nama_barang,
            "Modal": modal
        }
    ])

    df = pd.concat([df, data_baru], ignore_index=True)
    df.to_excel(FILE_EXCEL, index=False)

    st.success("Data tersimpan")

st.subheader("Daftar Barang")

df = pd.read_excel(FILE_EXCEL)
st.dataframe(df, use_container_width=True)
