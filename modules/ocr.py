import re
import cv2
import numpy as np
import easyocr

# Load OCR sekali saat aplikasi start
reader = easyocr.Reader(
    ['id', 'en'],
    gpu=False
)

# =========================
# CEK BLUR
# =========================
def blur_score(image):

    gray = cv2.cvtColor(
        np.array(image),
        cv2.COLOR_RGB2GRAY
    )

    return cv2.Laplacian(
        gray,
        cv2.CV_64F
    ).var()


# =========================
# PREPROCESS UMUM
# =========================
def preprocess(image):

    img = np.array(image)

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_RGB2GRAY
    )

    gray = cv2.resize(
        gray,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC
    )

    gray = cv2.equalizeHist(gray)

    return gray


# =========================
# PREPROCESS KTP HD
# =========================
def preprocess_ktp(image):

    img = np.array(image)

    img = cv2.resize(
        img,
        None,
        fx=3,
        fy=3,
        interpolation=cv2.INTER_CUBIC
    )

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_RGB2GRAY
    )

    gray = cv2.equalizeHist(gray)

    gray = cv2.GaussianBlur(
        gray,
        (3, 3),
        0
    )

    kernel = np.array([
        [-1, -1, -1],
        [-1,  9, -1],
        [-1, -D(
        gray,
        -1,
        kernel
    )

    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    return thresh


# =========================
# OCR UMUM
# =========================
def scan_text(image):

    processed = preprocess(image)

    result = reader.readtext(
        processed,
        detail=0,
        paragraph=True
    )

    return "\n".join(result)


# =========================
# CARI NIK
# =========================
def extract_nik(text):

    niks = re.findall(
        r"\d{16}",
        text
    )

    if len(niks) > 0:
        return niks[0]

    return "-"


# =========================
# OCR KTP HD
# =========================
def scan_ktp(image):

    processed = preprocess_ktp(image)

    result = reader.readtext(
        processed,
        detail=0,
        paragraph=False
    )

    raw_text = "\n".join(result)

    nik = extract_nik(raw_text)

    hasil = []

    hasil.append("=== DATA KTP ===")
    hasil.append("")
    hasil.append(f"NIK : {nik}")
    hasil.append("")

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
        "LAHIR",
        "JENIS KELAMIN",
        "KEWARGANEGARAAN"
    ]

    for line in raw_text.split("\n"):

        up = line.upper()

        for keyword in keywords:

            if keyword in up:
                hasil.append(line.strip())
                break

    hasil.append("")
    hasil.append("=== OCR MENTAH ===")
    hasil.append(raw_text)

    return "\n".join(hasil)
