import streamlit as st
from PIL import Image

from modules.ocr import scan_text, scan_ktp

st.set_page_config(
    page_title="OCR Scanner",
    page_icon="📷",
    layout="wide"
)

st.title("📷 OCR Scanner")

mode = st.radio(
    "Pilih Mode OCR",
    ["OCR Umum", "OCR KTP"],
    horizontal=True
)

photo = st.camera_input(
    "Ambil Foto"
)

if photo:

    image = Image.open(photo)

    st.image(
        image,
        caption="Foto Sumber",
        use_container_width=True
    )

    with st.spinner("Memproses OCR..."):

        if mode == "OCR KTP":
            text = scan_ktp(image)
        else:
            text = scan_text(image)

    st.subheader("📋 Hasil OCR")

    st.text_area(
        "Tekan lama lalu pilih Copy",
        value=text,
        height=350
    )

    st.success("OCR selesai")

    st.download_button(
        label="📄 Download TXT",
        data=text,
        file_name="hasil_ocr.txt",
        mime="text/plain"
    )
