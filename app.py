import streamlit as st
from PIL import Image

from modules.ocr import (
    scan_text,
    scan_ktp,
    blur_score
)

st.set_page_config(
    page_title="OCR Scanner",
    page_icon="📷",
    layout="wide"
)

st.title("📷 OCR Scanner HD")

mode = st.radio(
    "Pilih Mode OCR",
    [
        "OCR Umum",
        "OCR KTP HD"
    ],
    horizontal=True
)

st.info(
    "Tips: Dekatkan dokumen ke kamera dan pastikan pencahayaan cukup."
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

    score = blur_score(image)

    st.caption(
        f"Skor Ketajaman: {score:.0f}"
    )

    if score < 80:

        st.error(
            "Foto terlalu blur. Ulangi pengambilan foto."
        )

    else:

        with st.spinner("Memproses OCR..."):

            if mode == "OCR KTP HD":
                text = scan_ktp(image)
            else:
                text = scan_text(image)

        st.success("OCR selesai")

        st.subheader("📋 Hasil OCR")

        st.text_area(
            "Tekan lama lalu pilih Copy",
            value=text,
            height=350
        )

        st.download_button(
            label="📄 Download TXT",
            data=text,
            file_name="hasil_ocr.txt",
            mime="text/plain"
        )

        st.info(
            "Salin teks dengan tekan lama pada hasil OCR lalu pilih Copy."
        )
