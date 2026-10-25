import streamlit as st
import pandas as pd
import os
import uuid
import urllib.parse
from datetime import datetime

# ====================================
# KONFIGURASI
# ====================================

FILE_BARANG = "barang.xlsx"
FILE_TRANSAKSI = "transaksi.xlsx"

st.set_page_config(
    page_title="POS SINAR TERANG",
    page_icon="🏪",
    layout="wide"
)

st.title("🏪 POS TOKO SINAR TERANG")

# ====================================
# BUAT FILE JIKA BELUM ADA
# ====================================

if not os.path.exists(FILE_BARANG):
    pd.DataFrame(columns=[
        "ID",
        "Nama Barang",
        "Harga Jual"
    ]).to_excel(FILE_BARANG, index=False)

if not os.path.exists(FILE_TRANSAKSI):
    pd.DataFrame(columns=[
        "No Nota",
        "Tanggal",
        "Pelanggan",
        "No WA",
        "Nama Barang",
        "Harga",
        "Qty",
        "Subtotal"
    ]).to_excel(FILE_TRANSAKSI, index=False)

# ====================================
# SESSION
# ====================================

if "cart" not in st.session_state:
    st.session_state.cart = []

# ====================================
# MASTER BARANG
# ====================================

with st.expander("📦 Master Barang", expanded=False):

    with st.form("barang_form"):

        nama_barang = st.text_input("Nama Barang")

        harga_jual = st.number_input(
            "Harga Jual",
            min_value=0.0,
            step=100.0
        )

        simpan_barang = st.form_submit_button(
            "💾 Simpan Barang"
        )

    if simpan_barang:

        if nama_barang:

            df_barang = pd.read_excel(FILE_BARANG)

            data_baru = pd.DataFrame([{
                "ID": str(uuid.uuid4())[:8],
                "Nama Barang": nama_barang,
                "Harga Jual": harga_jual
            }])

            df_barang = pd.concat(
                [df_barang, data_baru],
                ignore_index=True
            )

            df_barang.to_excel(
                FILE_BARANG,
                index=False
            )

            st.success("Barang berhasil disimpan")

# ====================================
# DATA BARANG
# ====================================

df_barang = pd.read_excel(FILE_BARANG)

# ====================================
# PELANGGAN
# ====================================

st.subheader("👤 Data Pelanggan")

col1, col2 = st.columns(2)

with col1:
    pelanggan = st.text_input(
        "Nama Pelanggan (Opsional)"
    )

with col2:
    no_wa = st.text_input(
        "Nomor WhatsApp (Opsional)"
    )

if pelanggan.strip() == "":
    pelanggan = "UMUM"

if no_wa.strip() == "":
    no_wa = "-"

st.divider()

# ====================================
# TRANSAKSI
# ====================================

st.subheader("🛒 Transaksi")

if len(df_barang) > 0:

    col1, col2 = st.columns(2)

    with col1:

        barang = st.selectbox(
            "Pilih Barang",
            df_barang["Nama Barang"]
        )

    harga = df_barang.loc[
        df_barang["Nama Barang"] == barang,
        "Harga Jual"
    ].iloc[0]

    with col2:

        qty = st.number_input(
            "Jumlah",
            min_value=1,
            value=1
        )

    subtotal = harga * qty

    st.info(
        f"Subtotal : Rp {subtotal:,.0f}"
    )

    if st.button("➕ Tambah ke Keranjang"):

        st.session_state.cart.append({
            "Nama Barang": barang,
            "Harga": harga,
            "Qty": qty,
            "Subtotal": subtotal
        })

        st.success("Barang ditambahkan")

else:
    st.warning(
        "Silakan tambahkan barang terlebih dahulu"
    )

# ====================================
# KERANJANG
# ====================================

st.divider()

st.subheader("📋 Keranjang")

if len(st.session_state.cart) > 0:

    cart_df = pd.DataFrame(
        st.session_state.cart
    )

    st.dataframe(
        cart_df,
        use_container_width=True
    )

    total = cart_df["Subtotal"].sum()

    st.success(
        f"TOTAL BELANJA : Rp {total:,.0f}"
    )

    if st.button("💾 Simpan Transaksi"):

        no_nota = (
            "ST-" +
            datetime.now().strftime("%Y%m%d%H%M%S")
        )

        tanggal = datetime.now().strftime(
            "%d-%m-%Y %H:%M"
        )

        df_transaksi = pd.read_excel(
            FILE_TRANSAKSI
        )

        for item in st.session_state.cart:

            df_transaksi = pd.concat([
                df_transaksi,
                pd.DataFrame([{
                    "No Nota": no_nota,
                    "Tanggal": tanggal,
                    "Pelanggan": pelanggan,
                    "No WA": no_wa,
                    "Nama Barang": item["Nama Barang"],
                    "Harga": item["Harga"],
                    "Qty": item["Qty"],
                    "Subtotal": item["Subtotal"]
                }])
            ])

        df_transaksi.to_excel(
            FILE_TRANSAKSI,
            index=False
        )

        st.success(
            f"Transaksi berhasil disimpan - {no_nota}"
        )

        # =====================
        # NOTA
        # =====================

        nota = f"""
🏪 TOKO SINAR TERANG

No Nota : {no_nota}
Tanggal : {tanggal}

Pelanggan : {pelanggan}

"""

        for item in st.session_state.cart:

            nota += (
                f"\n{item['Nama Barang']}"
                f"\n{item['Qty']} x Rp {item['Harga']:,.0f}"
                f" = Rp {item['Subtotal']:,.0f}\n"
            )

        nota += (
            f"\n===================="
            f"\nTOTAL : Rp {total:,.0f}"
            f"\n===================="
            f"\nTerima kasih 🙏"
        )

        st.text_area(
            "🧾 Nota Digital",
            nota,
            height=350
        )

        if no_wa != "-":

            nomor = no_wa.replace(
                "+",
                ""
            ).replace(
                " ",
                ""
            )

            wa_link = (
                "https://wa.me/"
                + nomor
                + "?text="
                + urllib.parse.quote(nota)
            )

            st.link_button(
                "📱 Kirim Nota ke WhatsApp",
                wa_link
            )

        st.session_state.cart = []

else:

    st.info(
        "Keranjang masih kosong"
    )

# ====================================
# LAPORAN HARI INI
# ====================================

st.divider()

st.subheader("📊 Ringkasan")

if os.path.exists(FILE_TRANSAKSI):

    laporan = pd.read_excel(
        FILE_TRANSAKSI
    )

    if len(laporan) > 0:

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Jumlah Transaksi",
                laporan["No Nota"].nunique()
            )

        with col2:
            st.metric(
                "Item Terjual",
                int(
                    laporan["Qty"].sum()
                )
            )

        with col3:
            st.metric(
                "Total Omzet",
                f"Rp {laporan['Subtotal'].sum():,.0f}"
            )
