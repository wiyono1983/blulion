import streamlit as st
import pandas as pd
import os
import io
import uuid
import urllib.parse

from datetime import datetime
from openpyxl import load_workbook

# =====================================================
# KONFIGURASI APP
# =====================================================

st.set_page_config(
    page_title="POS Sinar Terang",
    page_icon="🏪",
    layout="wide"
)

st.title("🏪 POS SINAR TERANG")

# =====================================================
# FOLDER DATA
# =====================================================

DATA_DIR = "data"

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

MASTER_BARANG_FILE = os.path.join(
    DATA_DIR,
    "master_barang.xlsx"
)

TRANSAKSI_FILE = os.path.join(
    DATA_DIR,
    "transaksi.xlsx"
)

SETTING_FILE = os.path.join(
    DATA_DIR,
    "setting.xlsx"
)

# =====================================================
# BUAT FILE DEFAULT
# =====================================================

def init_master_barang():

    if not os.path.exists(MASTER_BARANG_FILE):

        df = pd.DataFrame(columns=[
            "ID",
            "Nama Barang",
            "Harga Modal",

            "Metode Harga",

            "Margin Profit (%)",
            "Margin Nominal",

            "Harga Grosir",
            "Harga Reseller",
            "Harga Retail",
            "Harga Olshop",

            "Fee Olshop (%)",

            "Harga Jual Aktif"
        ])

        df.to_excel(
            MASTER_BARANG_FILE,
            index=False
        )

def init_transaksi():

    if not os.path.exists(TRANSAKSI_FILE):

        df = pd.DataFrame(columns=[
            "No Nota",
            "Tanggal",

            "Pelanggan",
            "No WA",

            "Nama Barang",

            "Harga Modal",
            "Harga Jual",

            "Qty",

            "Subtotal",
            "Laba"
        ])

        df.to_excel(
            TRANSAKSI_FILE,
            index=False
        )

def init_setting():

    if not os.path.exists(SETTING_FILE):

        setting = pd.DataFrame([{
            "Margin Grosir":10,
            "Margin Reseller":20,
            "Margin Retail":30,

            "Margin Olshop":20,
            "Fee Olshop":8
        }])

        setting.to_excel(
            SETTING_FILE,
            index=False
        )

# Jalankan saat startup

init_master_barang()
init_transaksi()
init_setting()

# =====================================================
# HELPER
# =====================================================

def load_barang():

    return pd.read_excel(
        MASTER_BARANG_FILE
    )

def save_barang(df):

    df.to_excel(
        MASTER_BARANG_FILE,
        index=False
    )

def load_transaksi():

    return pd.read_excel(
        TRANSAKSI_FILE
    )

def save_transaksi(df):

    df.to_excel(
        TRANSAKSI_FILE,
        index=False
    )

def load_setting():

    return pd.read_excel(
        SETTING_FILE
    )
def save_setting(df):

    df.to_excel(
        SETTING_FILE,
        index=False
    )

def format_rupiah(nilai):

    return (
        "Rp {:,.0f}"
        .format(nilai)
        .replace(",", ".")
    )

def generate_nota():

    return (
        "ST-"
        + datetime.now()
        .strftime("%Y%m%d%H%M%S")
    )

# =====================================================
# SESSION STATE
# =====================================================

if "cart" not in st.session_state:
    st.session_state.cart = []

# =====================================================
# LOAD DATA
# =====================================================

df_barang = load_barang()
df_transaksi = load_transaksi()
df_setting = load_setting()

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("🏪 SINAR TERANG")

    st.caption(
        "POS & Laporan Penjualan"
    )

    menu = st.radio(
        "Menu",
        [
            "🏪 Dashboard",
            "📦 Master Barang",
            "🛒 Transaksi",
            "📄 Riwayat",
            "📊 Laporan",
            "⚙️ Pengaturan"
        ]
    )

# =====================================================
# DASHBOARD
# =====================================================

if menu == "🏪 Dashboard":

    st.subheader(
        "Ringkasan Usaha"
    )

    omzet = 0
    laba = 0

    if len(df_transaksi) > 0:

        omzet = (
            df_transaksi["Subtotal"]
            .sum()
        )

        laba = (
            df_transaksi["Laba"]
            .sum()
        )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Barang",
            len(df_barang)
        )

    with col2:

        st.metric(
            "Total Transaksi",
            len(
                df_transaksi["No Nota"]
                .unique()
            )
            if len(df_transaksi) > 0
            else 0
        )

    with col3:

        st.metric(
            "Omzet",
            format_rupiah(
                omzet
            )
        )

    with col4:

        st.metric(
            "Laba",
            format_rupiah(
                laba
            )
        )

    st.divider()

    st.info(
        """
        Selamat datang di POS Sinar Terang.

        Silakan gunakan menu di sebelah kiri untuk mengelola:

        ✅ Master Barang

        ✅ Transaksi Penjualan

        ✅ Nota WhatsApp

        ✅ Laporan Penjualan

        ✅ Export Excel
        """
    )
# =====================================================
# MASTER BARANG
# =====================================================

if menu == "📦 Master Barang":

    st.subheader("📦 Master Barang")

    with st.form("form_barang"):

        nama_barang = st.text_input(
            "Nama Barang"
        )

        harga_modal = st.number_input(
            "Harga Modal",
            min_value=0.0,
            step=100.0
        )

        metode_harga = st.radio(
            "Metode Penentuan Harga",
            [
                "Margin Profit (%)",
                "Margin Nominal",
                "Harga Manual"
            ]
        )

        margin_profit = 0.0
        margin_nominal = 0.0
        harga_manual = 0.0

        if metode_harga == "Margin Profit (%)":

            margin_profit = st.number_input(
                "Target Margin Profit (%)",
                min_value=1.0,
                max_value=95.0,
                value=20.0
            )

        elif metode_harga == "Margin Nominal":

            margin_nominal = st.number_input(
                "Margin Nominal (Rp)",
                min_value=0.0,
                step=1000.0
            )

        else:

            harga_manual = st.number_input(
                "Harga Jual Manual",
                min_value=0.0,
                step=100.0
            )

        st.divider()

        setting = load_setting().iloc[0]

        margin_grosir = setting["Margin Grosir"]
        margin_reseller = setting["Margin Reseller"]
        margin_retail = setting["Margin Retail"]

        margin_olshop = setting["Margin Olshop"]
        fee_olshop = setting["Fee Olshop"]

        # ============================
        # REKOMENDASI HARGA
        # ============================

        harga_grosir = 0
        harga_reseller = 0
        harga_retail = 0
        harga_olshop = 0

        if harga_modal > 0:

            harga_grosir = (
                harga_modal /
                (1 - (margin_grosir / 100))
            )

            harga_reseller = (
                harga_modal /
                (1 - (margin_reseller / 100))
            )

            harga_retail = (
                harga_modal /
                (1 - (margin_retail / 100))
            )

            harga_olshop = (
                harga_modal /
                (
                    (1 - (fee_olshop / 100))
                    *
                    (1 - (margin_olshop / 100))
                )
            )

        st.subheader(
            "💡 Rekomendasi Harga"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.success(
                f"""
                Grosir
                {format_rupiah(harga_grosir)}
                """
            )

            st.success(
                f"""
                Reseller
                {format_rupiah(harga_reseller)}
                """
            )

        with col2:

            st.success(
                f"""
                Retail
                {format_rupiah(harga_retail)}
                """
            )

            st.success(
                f"""
                Olshop
                {format_rupiah(harga_olshop)}
                """
            )

        # ============================
        # HARGA AKHIR
        # ============================

        harga_jual = 0

        if (
            metode_harga ==
            "Margin Profit (%)"
        ):

            if margin_profit < 100:

                harga_jual = (
                    harga_modal /
                    (
                        1 -
                        (margin_profit / 100)
                    )
                )

        elif (
            metode_harga ==
            "Margin Nominal"
        ):

            harga_jual = (
                harga_modal +
                margin_nominal
            )

        else:

            harga_jual = harga_manual

        st.info(
            f"Harga Jual Aktif : "
            f"{format_rupiah(harga_jual)}"
        )

        simpan_barang = (
            st.form_submit_button(
                "💾 Simpan Barang"
            )
        )

    # ============================
    # SIMPAN
    # ============================

    if simpan_barang:

        if nama_barang.strip() == "":

            st.warning(
                "Nama barang wajib diisi"
            )

        else:

            df_barang = load_barang()

            data_baru = pd.DataFrame([{

                "ID":
                str(uuid.uuid4())[:8],

                "Nama Barang":
                nama_barang,

                "Harga Modal":
                round(harga_modal),

                "Metode Harga":
                metode_harga,

                "Margin Profit (%)":
                margin_profit,

                "Margin Nominal":
                margin_nominal,

                "Harga Grosir":
                round(harga_grosir),

                "Harga Reseller":
                round(harga_reseller),

                "Harga Retail":
                round(harga_retail),

                "Harga Olshop":
                round(harga_olshop),

                "Fee Olshop (%)":
                fee_olshop,

                "Harga Jual Aktif":
                round(harga_jual)

            }])

            df_barang = pd.concat(
                [df_barang, data_baru],
                ignore_index=True
            )

            save_barang(df_barang)

            st.success(
                "Barang berhasil disimpan"
            )

            st.rerun()

    st.divider()

    # ============================
    # DAFTAR BARANG
    # ============================

    st.subheader(
        "📋 Daftar Barang"
    )

    df_barang = load_barang()

    if len(df_barang) > 0:

        st.dataframe(
            df_barang,
            use_container_width=True
        )

    else:

        st.info(
            "Belum ada data"
        )

    st.divider()

    # ============================
    # HAPUS BARANG
    # ============================

    if len(df_barang) > 0:

        pilihan_barang = st.selectbox(
            "Pilih Barang Yang Akan Dihapus",
            df_barang["ID"]
            + " | "
            + df_barang["Nama Barang"]
        )

        if st.button(
            "🗑️ Hapus Barang"
        ):

            id_hapus = (
                pilihan_barang
                .split("|")[0]
                .strip()
            )

            df_barang = df_barang[
                df_barang["ID"]
                != id_hapus
            ]

            save_barang(df_barang)

            st.success(
                "Barang berhasil dihapus"
            )

            st.rerun()
# =====================================================
# TRANSAKSI
# =====================================================

# =====================================================
# TRANSAKSI
# =====================================================

if menu == "🛒 Transaksi":

    st.subheader("🛒 Transaksi Penjualan")

    col1, col2 = st.columns(2)

    with col1:

        pelanggan = st.text_input(
            "Nama Pelanggan"
        )

    with col2:

        no_wa = st.text_input(
            "WA Pelanggan (Opsional)"
        )

    if pelanggan.strip() == "":
        pelanggan = "UMUM"

    wa_tujuan = st.text_input(
        "Nomor WA Tujuan Nota"
    )

    st.divider()

    metode = st.radio(
        "Metode Input",
        [
            "Ambil Dari Master",
            "Input Manual"
        ],
        horizontal=True
    )

    # =========================
    # DARI MASTER
    # =========================

    if metode == "Ambil Dari Master":

        if len(df_barang) > 0:

            barang = st.selectbox(
                "Pilih Barang",
                df_barang["Nama Barang"]
            )

            data_barang = df_barang[
                df_barang["Nama Barang"]
                == barang
            ].iloc[0]

            jenis_harga = st.selectbox(
                "Jenis Harga",
                [
                    "Aktif",
                    "Grosir",
                    "Reseller",
                    "Retail",
                    "Olshop"
                ]
            )

            harga_jual = (
                data_barang["Harga Jual Aktif"]
            )

            if jenis_harga == "Grosir":
                harga_jual = data_barang["Harga Grosir"]

            elif jenis_harga == "Reseller":
                harga_jual = data_barang["Harga Reseller"]

            elif jenis_harga == "Retail":
                harga_jual = data_barang["Harga Retail"]

            elif jenis_harga == "Olshop":
                harga_jual = data_barang["Harga Olshop"]

            qty = st.number_input(
                "Qty",
                min_value=1,
                value=1
            )

            subtotal = harga_jual * qty

            st.info(
                f"Subtotal : {format_rupiah(subtotal)}"
            )

            if st.button("➕ Tambah Barang"):

                st.session_state.cart.append({

                    "Nama Barang":
                    barang,

                    "Harga Modal":
                    data_barang["Harga Modal"],

                    "Harga Jual":
                    harga_jual,

                    "Qty":
                    qty,

                    "Subtotal":
                    subtotal,

                    "Laba":
                    (
                        harga_jual
                        -
                        data_barang["Harga Modal"]
                    ) * qty

                })

                st.rerun()

    # =========================
    # MANUAL
    # =========================

    else:

        nama_barang = st.text_input(
            "Nama Barang"
        )

        harga_modal = st.number_input(
            "Harga Modal",
            min_value=0.0
        )

        harga_jual = st.number_input(
            "Harga Jual",
            min_value=0.0
        )

        qty = st.number_input(
            "Qty",
            min_value=1,
            value=1
        )

        subtotal = harga_jual * qty

        if st.button(
            "➕ Tambah Manual"
        ):

            st.session_state.cart.append({

                "Nama Barang":
                nama_barang,

                "Harga Modal":
                harga_modal,

                "Harga Jual":
                harga_jual,

                "Qty":
                qty,

                "Subtotal":
                subtotal,

                "Laba":
                (
                    harga_jual -
                    harga_modal
                ) * qty

            })

            st.rerun()

    st.divider()

    # =========================
    # KERANJANG
    # =========================

    if len(st.session_state.cart) > 0:

        cart_df = pd.DataFrame(
            st.session_state.cart
        )

        st.subheader("🧺 Keranjang")

        st.dataframe(
            cart_df,
            use_container_width=True
        )

        total = cart_df[
            "Subtotal"
        ].sum()

        total_laba = cart_df[
            "Laba"
        ].sum()

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Total Belanja",
                format_rupiah(total)
            )

        with col2:

            st.metric(
                "Estimasi Laba",
                format_rupiah(total_laba)
            )

        # ====================
        # SIMPAN
        # ====================

        if st.button(
            "💾 Simpan Transaksi"
        ):

            no_nota = generate_nota()

            st.session_state.last_nota = (
                no_nota
            )

            tanggal = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            trx = load_transaksi()

            for item in st.session_state.cart:

                trx = pd.concat(
                    [
                        trx,
                        pd.DataFrame([{

                            "No Nota":
                            no_nota,

                            "Tanggal":
                            tanggal,

                            "Pelanggan":
                            pelanggan,

                            "No WA":
                            no_wa,

                            "Nama Barang":
                            item["Nama Barang"],

                            "Harga Modal":
                            item["Harga Modal"],

                            "Harga Jual":
                            item["Harga Jual"],

                            "Qty":
                            item["Qty"],

                            "Subtotal":
                            item["Subtotal"],

                            "Laba":
                            item["Laba"]

                        }])
                    ],
                    ignore_index=True
                )

            save_transaksi(trx)

            st.success(
                f"Transaksi {no_nota} disimpan"
            )

        # ====================
        # NOTA
        # ====================

        no_nota_tampil = (
            st.session_state.last_nota
            if st.session_state.last_nota
            else generate_nota()
        )

        tanggal_nota = datetime.now().strftime(
            "%d-%m-%Y %H:%M"
        )

        nota = (
            f"TOKO SINAR TERANG\n"
            f"No Nota : {no_nota_tampil}\n"
            f"Tanggal : {tanggal_nota}\n"
            f"Pelanggan : {pelanggan}\n"
        )

        if no_wa.strip():
            nota += f"WA : {no_wa}\n"

        nota += "\n"

        for item in st.session_state.cart:

            nota += (
                f"{item['Nama Barang']}\n"
                f"{item['Qty']} x "
                f"{format_rupiah(item['Harga Jual'])}"
                f" = "
                f"{format_rupiah(item['Subtotal'])}\n"
            )

        nota += (
            "\n"
            f"TOTAL : {format_rupiah(total)}\n"
            "\n"
            "Terima kasih 🙏"
        )

        st.subheader(
            "🧾 Nota Siap Kirim"
        )

        st.text_area(
            "Nota",
            nota,
            height=220
        )

        st.code(
            nota,
            language=None
        )

        # ====================
        # WHATSAPP
        # ====================

        if wa_tujuan.strip():

            nomor = (
                wa_tujuan
                .replace("+", "")
                .replace(" ", "")
            )

            wa_url = (
                "https://wa.me/"
                + nomor
                + "?text="
                + urllib.parse.quote(nota)
            )

            st.link_button(
                "📱 Kirim Nota ke WhatsApp",
                wa_url
            )

    else:

        st.info(
            "Keranjang masih kosong"
        )


# =====================================================
# RIWAYAT TRANSAKSI
# =====================================================

if menu == "📄 Riwayat":

    st.subheader("📄 Riwayat Transaksi")

    transaksi = load_transaksi()

    if len(transaksi) == 0:

        st.info(
            "Belum ada transaksi"
        )

    else:

        cari_nota = st.text_input(
            "Cari No Nota"
        )

        cari_pelanggan = st.text_input(
            "Cari Pelanggan"
        )

        tampil = transaksi.copy()

        if cari_nota:

            tampil = tampil[
                tampil["No Nota"]
                .astype(str)
                .str.contains(
                    cari_nota,
                    case=False,
                    na=False
                )
            ]

        if cari_pelanggan:

            tampil = tampil[
                tampil["Pelanggan"]
                .astype(str)
                .str.contains(
                    cari_pelanggan,
                    case=False,
                    na=False
                )
            ]

        st.dataframe(
            tampil,
            use_container_width=True
        )

        st.divider()

        daftar_nota = (
            transaksi["No Nota"]
            .dropna()
            .unique()
            .tolist()
        )

        nota_detail = st.selectbox(
            "Lihat Detail Nota",
            daftar_nota
        )

        detail = transaksi[
            transaksi["No Nota"]
            == nota_detail
        ]

        if len(detail) > 0:

            total_nota = (
                detail["Subtotal"]
                .sum()
            )

            laba_nota = (
                detail["Laba"]
                .sum()
            )

            st.subheader(
                "Detail Transaksi"
            )

            st.dataframe(
                detail,
                use_container_width=True
            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Total",
                    format_rupiah(
                        total_nota
                    )
                )

            with col2:

                st.metric(
                    "Laba",
                    format_rupiah(
                        laba_nota
                    )
                )

# =====================================================
# LAPORAN
# =====================================================

if menu == "📊 Laporan":

    st.subheader(
        "📊 Laporan Penjualan"
    )

    trx = load_transaksi()

    if len(trx) == 0:

        st.info(
            "Belum ada transaksi"
        )

    else:

        # ==========================
        # KPI
        # ==========================

        omzet = trx[
            "Subtotal"
        ].sum()

        laba = trx[
            "Laba"
        ].sum()

        transaksi_unik = len(
            trx["No Nota"]
            .unique()
        )

        qty_total = trx[
            "Qty"
        ].sum()

        col1, col2, col3, col4 = (
            st.columns(4)
        )

        with col1:

            st.metric(
                "Omzet",
                format_rupiah(
                    omzet
                )
            )

        with col2:

            st.metric(
                "Laba",
                format_rupiah(
                    laba
                )
            )

        with col3:

            st.metric(
                "Transaksi",
                transaksi_unik
            )

        with col4:

            st.metric(
                "Item Terjual",
                int(qty_total)
            )

        st.divider()

        # ==========================
        # PRODUK TERLARIS
        # ==========================

        st.subheader(
            "🏆 Produk Terlaris"
        )

        produk_terlaris = (

            trx.groupby(
                "Nama Barang"
            )["Qty"]
            .sum()
            .reset_index()
            .sort_values(
                "Qty",
                ascending=False
            )

        )

        st.dataframe(
            produk_terlaris.head(10),
            use_container_width=True
        )

        st.divider()

        # ==========================
        # PRODUK PALING UNTUNG
        # ==========================

        st.subheader(
            "💰 Produk Paling Untung"
        )

        produk_untung = (

            trx.groupby(
                "Nama Barang"
            )["Laba"]
            .sum()
            .reset_index()
            .sort_values(
                "Laba",
                ascending=False
            )

        )

        st.dataframe(
            produk_untung.head(10),
            use_container_width=True
        )

        st.divider()

        # ==========================
        # CUSTOMER TERBAIK
        # ==========================

        st.subheader(
            "👤 Pelanggan Teratas"
        )

        pelanggan = trx[
            trx["Pelanggan"]
            != "UMUM"
        ]

        if len(pelanggan) > 0:

            pelanggan_top = (

                pelanggan
                .groupby(
                    "Pelanggan"
                )
                ["Subtotal"]
                .sum()
                .reset_index()
                .sort_values(
                    "Subtotal",
                    ascending=False
                )

            )

            st.dataframe(
                pelanggan_top,
                use_container_width=True
            )

        else:

            st.info(
                "Belum ada data pelanggan"
            )

        st.divider()

        # ==========================
        # GRAFIK
        # ==========================

        st.subheader(
            "📈 Grafik Penjualan"
        )

        trx["TanggalOnly"] = pd.to_datetime(
            trx["Tanggal"]
        ).dt.date

        grafik = (

            trx.groupby(
                "TanggalOnly"
            )
            ["Subtotal"]
            .sum()
            .reset_index()

        )

        grafik = grafik.set_index(
            "TanggalOnly"
        )

        st.line_chart(
            grafik
        )
# =====================================================
# PENGATURAN
# =====================================================

if menu == "⚙️ Pengaturan":

    st.subheader(
        "⚙️ Pengaturan Sistem"
    )

    setting = load_setting()

    data = setting.iloc[0]

    with st.form("setting_form"):

        margin_grosir = st.number_input(
            "Margin Grosir (%)",
            value=float(
                data["Margin Grosir"]
            )
        )

        margin_reseller = st.number_input(
            "Margin Reseller (%)",
            value=float(
                data["Margin Reseller"]
            )
        )

        margin_retail = st.number_input(
            "Margin Retail (%)",
            value=float(
                data["Margin Retail"]
            )
        )

        margin_olshop = st.number_input(
            "Margin Olshop (%)",
            value=float(
                data["Margin Olshop"]
            )
        )

        fee_olshop = st.number_input(
            "Fee Marketplace (%)",
            value=float(
                data["Fee Olshop"]
            )
        )

        simpan_setting = (
            st.form_submit_button(
                "💾 Simpan Pengaturan"
            )
        )

    if simpan_setting:

        df_setting = pd.DataFrame([{

            "Margin Grosir":
            margin_grosir,

            "Margin Reseller":
            margin_reseller,

            "Margin Retail":
            margin_retail,

            "Margin Olshop":
            margin_olshop,

            "Fee Olshop":
            fee_olshop

        }])

        save_setting(
            df_setting
        )

        st.success(
            "Pengaturan berhasil disimpan"
        )

        st.rerun()
