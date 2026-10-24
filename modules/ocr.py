import cv2
import easyocr
import numpy as np
import re

# Load OCR sekali saja
reader = easyocr.Reader(
    ['id', 'en'],
    gpu=False
)


def preprocess(image):
    """
    Meningkatkan kualitas gambar sebelum OCR
    """

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
    """
    OCR umum
    """

    processed = preprocess(image)

    results = reader.readtext(
        processed,
        detail=0,
        paragraph=True
    )

    return "\n".join(results)


def find_nik(text):
    """
    Cari NIK 16 digit
    """

    nik_list = re.findall(r"\d{16}", text)

    if nik_list:
        return nik_list[0]

    return "-"


def scan_ktp(image):
    """
    OCR khusus KTP
    """

    processed = preprocess(image)

    results = reader.readtext(
        processed,
        detail=0,
        paragraph=False
    )

    raw_text = "\n".join(results)

    nik = find_nik(raw_text)

    output = []

    output.append("=== DATA KTP ===")
    output.append(f"NIK : {nik}")

    keywords = [
        "NAMA",
        "ALAMAT",
        "RT/RW",
        "KEL",
        "DESA",
        "KECAMATAN",
        "AGAMA",
        "STATUS",
        "PEKERJAAN",
        "KEWARGANEGARAAN",
        "LAHIR",
        "JENIS KELAMIN"
    ]

    for line in raw_text.split("\n"):

        upper = line.upper()

        for keyword in keywords:

            if keyword in upper:
                output.append(line.strip())
                break

    output.append("")
    output.append("=== OCR MENTAH ===")
    output.append(raw_text)

    return "\n".join(output)
