import cv2
import easyocr
import numpy as np
import re

# Inisialisasi OCR
reader = easyocr.Reader(
    ['id', 'en'],
    gpu=False
)

def preprocess(image):

    img = np.array(image)

    # Perbesar gambar
    img = cv2.resize(
        img,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC
    )

    # Grayscale
    gray = cv2.cvtColor(
        img,
        cv2.COLOR_RGB2GRAY
    )

    # Hilangkan noise
    gray = cv2.GaussianBlur(
        gray,
        (3, 3),
        0
    )

    # Tingkatkan kontras
    gray = cv2.equalizeHist(gray)

    # Threshold
    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    return thresh


def scan_text(image):

    processed = preprocess(image)

    result = reader.readtext(
        processed,
        detail=0,
        paragraph=True
    )

    return "\n".join(result)


def extract_nik(text):

    kandidat = re.findall(r"\d{16}", text)

    if kandidat:
        return kandidat[0]

    return "-"


def scan_ktp(image):

    processed = preprocess(image)

    result = reader.readtext(
        processed,
        detail=0,
        paragraph=False
    )

    lines = []

    for item in result:
        if isinstance(item, str):
            lines.append(item)
        else:
            lines.append(str(item))

    text = "\n".join(lines)

    nik = extract_nik(text)

    hasil = []
    hasil.append(f"NIK : {nik}")

    keywords = [
        "NAMA",
        "TEMPAT",
        "LAHIR",
        "ALAMAT",
        "RT/RW",
        "KEL",
        "DESA",
        "KECAMATAN",
        "AGAMA",
        "STATUS",
        "PEKERJAAN",
        "KEWARGANEGARAAN"
    ]

    for line in text.split("\n"):

        line_upper = line.upper()

        for keyword in keywords:

            if keyword in line_upper:
                hasil.append(line.strip())
                break

    if len(hasil) == 1:
        return text

    return "\n".join(hasil)
