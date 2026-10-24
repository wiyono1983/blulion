import streamlit as st
from PIL import Image

from modules.ocr import scan_text
from modules.whatsapp import create_link

st.set_page_config(
    page_title="OCR WhatsApp Scanner"
)

st.title("📷 OCR WhatsApp Scanner")

photo = st.camera_input("Ambil Foto")

if photo:

    image = Image.open(photo)

    text = scan_text(image)

    st.text_area(
        "Hasil OCR",
        text,
        height=300
    )

    st.link_button(
        "📱 Kirim ke WhatsApp",
        create_link(text)
    )
