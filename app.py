import streamlit as st
import pandas as pd
import os
import uuid

# =====================
# Konfigurasi
# =====================

FILE_EXCEL = "data_barang.xlsx"

st.set_page_config(
    page_title="POS Toko",
    page_icon="📦",
    layout="wide"
)

st.title("📦 POS Toko Sederhana")

# =====================
# Buat file jika belum ada
# =====================

if not os.path.exists(FILE_EXCEL):

    df_awal = pd.DataFrame(columns=[
        "ID",
        "Nama Barang",
        "Modal",
        "Margin (%)",
        "Harga Jual"
    ])

    df_awal.to_excel(FILE_EXCEL, index=False)

# =====================
# Form Tambah Barang
# =====================

st.subheader("➕ Tambah Barang")

with st.form("form_barang"):

    nama_barang = st.text_input("Nama Barang")

    modal = st.number_input(
        "Harga Modal",
        min_value=0.0,
        step=100.0
    )

    margin = st.selectbox(
        "Margin (%)",
        [20, 25, 30, 40, 50, 75, 100],
        index=2
    )

    harga_preview = modal + (modal * margin / 100)

    st.info(
        f"Harga Jual Otomatis : Rp {harga_preview:,.0f}"
    )

    simpan = st.form_submit_button("💾 Simpan")

if simpan:

    if nama_barang.strip() == "":
        st.warning("Nama barang wajib diisi")

    else:

        harga_jual = modal + (modal * margin / 100)

        df = pd.read_excel(FILE_EXCEL)

        data_baru = pd.DataFrame([{
            "ID": str(uuid.uuid4())[:8],
            "Nama Barang": nama_barang,
            "Modal": modal,
            "Margin (%)": margin,
            "Harga Jual": round(harga_jual)
        }])

        df = pd.concat(
            [df, data_baru],
            ignore_index=True
        )

        df.to_excel(FILE_EXCEL, index=False)

        st.success(
            f"{nama_barang} berhasil disimpan"
        )

# =====================
# Tampilkan Data
# =====================

st.divider()

st.subheader("📋 Daftar Barang")

df = pd.read_excel(FILE_EXCEL)

if len(df) > 0:

    st.dataframe(
        df,
        use_container_width=True
    )

else:

    st.info("Belum ada data barang")

# =====================
# Hapus Barang
# =====================

st.divider()

st.subheader("🗑️ Hapus Barang")

if len(df) > 0:

    pilihan = st.selectbox(
        "Pilih Barang",
        df["ID"] + " - " + df["Nama Barang"]
    )

    if st.button("Hapus Barang"):

        id_hapus = pilihan.split(" - ")[0]

        df = df[df["ID"] != id_hapus]

        df.to_excel(
            FILE_EXCEL,
            index=False
        )

        st.success("Barang berhasil dihapus")

        st.rerun()

# =====================
# Ringkasan
# =====================

st.divider()

if len(df) > 0:

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Jumlah Barang",
            len(df)
        )

    with col2:
        st.metric(
            "Total Modal",
            f"Rp {df['Modal'].sum():,.0f}"
        )

    with col3:
        st.metric(
            "Total Nilai Jual",
            f"Rp {df['Harga Jual'].sum():,.0f}"
        )
