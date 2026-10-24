import cv2
import easyocr
import numpy as np
import re

# OCR Reader
reader = easyocr.Reader(
    ['id', 'en'],
    gpu=False
)

# ==========================
# CEK BLUR
# ==========================
def blur_score(image):

    gray = cv2.cvtColor(
        np.array(image),
        cv2.COLOR_RGB2GRAY
    )

    return cv2.Laplacian(
        gray,
        cv2.CV_64F
    ).var()


# ==========================
# PREPROCESS HD
# ==========================
def preprocess_hd(image):

    img = np.array(image)

    # Upscale HD
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

    # Contrast
    gray = cv2.equalizeHist(gray)

    # Denoise
    gray = cv2.fastNlMeansDenoising(
        gray,
        None,
        10,
        7,
        21
    )

    # Sharpen
    kernel = np.array([
        [-1,-1,-1],
        [-1, 9,-1],
        [-1,-1,-1]
    ])

    sharp = cv2.filter2D(
        gray,
        -1,
        kernel
    )

    # Adaptive Threshold
    thresh = cv2.adaptiveThreshold(
        sharp,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        15,
        5
    )

    return thresh


# ==========================
# OCR UMUM
# ==========================
def scan_text(image):

    processed = preprocess_hd(image)

    results = reader.readtext(
        processed,
        detail=0,
        paragraph=True
    )

    return "\n".join(results)


# ==========================
# CARI NIK
# ==========================
def extract_nik(text):

    nik = re.findall(
        r"\d{16}",
        text
    )

    if nik:
        return nik[0]

    return "-"


# ==========================
# OCR KTP HD
# ==========================
def scan_ktp(image):

    processed = preprocess_hd(image)

    results = reader.readtext(
        processed,
        detail=0,
        paragraph=False
    )

    raw_text = "\n".join(results)

    nik = extract_nik(raw_text)

    output = []

    output.append("=== HASIL OCR KTP HD ===")
    output.append("")

    output.append(f"NIK : {nik}")
    output.append("")

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
        "KEWARGANEGARAAN",
        "JENIS KELAMIN",
        "GOL",
        "DARAH"
    ]

    for line in raw_text.split("\n"):

        upper = line.upper()

        for keyword in keywords:

            if keyword in upper:
                output.append(line.strip())
                break

    output.append("")
    output.append("========== OCR MENTAH ==========")
    output.append(raw_text)

    return "\n".join(output)
