import streamlit as st
from PIL import Image

from modules.ocr import scan_text

st.set_page_config(
    page_title="OCR Scanner",
    page_icon="📷",
    layout="wide"
)

st.title("📷 OCR Scanner")

photo = st.camera_input("Ambil Foto")

if photo:

    image = Image.open(photo)

    with st.spinner("Sedang membaca teks..."):
        text = scan_text(image)

    st.subheader("📋 Hasil OCR")

    st.text_area(
        label="Tekan lama pada teks lalu pilih Copy",
        value=text,
        height=300
    )

    st.code(text, language=None)

    st.success("OCR selesai. Anda bisa langsung menyalin hasil teks.")
