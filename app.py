import streamlit as st
from PIL import Image

from modules.ocr import scan_text, scan_ktp, blur_score

st.set_page_config(
    page_title="OCR Scanner",
    page_icon="📷"
)

st.title("📷 OCR Scanner")

mode = st.radio(
    "Mode OCR",
    ["OCR Umum", "OCR KTP HD"],
    horizontal=True
)

source = st.radio(
    "Sumber Gambar",
    ["📷 Kamera", "🖼️ Galeri"],
    horizontal=True
)

image = None

if source == "📷 Kamera":

    photo = st.camera_input(
        "Ambil Foto"
    )

    if photo:
        image = Image.open(photo)

else:

    file = st.file_uploader(
        "Pilih Gambar",
        type=["jpg", "jpeg", "png"]
    )

    if file:
        image = Image.open(file)

if image:

    st.image(
        image,
        caption="Gambar",
        use_container_width=True
    )

    skor = blur_score(image)

    st.write(
        f"Skor Ketajaman: {skor:.0f}"
    )

    with st.spinner("Memproses OCR..."):

        if mode == "OCR KTP HD":
            hasil = scan_ktp(image)
        else:
            hasil = scan_text(image)

    st.text_area(
        "Hasil OCR",
        value=hasil,
        height=350
    )

    st.download_button(
        "📄 Download TXT",
        hasil,
        file_name="hasil_ocr.txt"
    )
