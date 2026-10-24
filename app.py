import streamlit as st
from PIL import Image

from modules.ocr import scan_text, scan_ktp, blur_score

st.set_page_config(
    page_title="OCR Scanner",
    page_icon="📷"
)

st.title("📷 OCR Scanner")

mode = st.radio(
    "Pilih Mode OCR",
    ["OCR Umum", "OCR KTP HD"]
)

photo = st.camera_input("Ambil Foto")

if photo:

    image = Image.open(photo)

    score = blur_score(image)

    st.write(f"Skor Ketajaman: {score:.0f}")

    if mode == "OCR KTP HD":
        text = scan_ktp(image)
    else:
        text = scan_text(image)

    st.text_area(
        "Hasil OCR",
        value=text,
        height=300
    )
