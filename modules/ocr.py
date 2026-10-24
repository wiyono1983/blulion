import easyocr
import numpy as np

reader = easyocr.Reader(['id', 'en'], gpu=False)

def blur_score(image):
    return 100

def scan_text(image):

    img = np.array(image)

    result = reader.readtext(
        img,
        detail=0,
        paragraph=True
    )

    return "\n".join(result)

def scan_ktp(image):

    img = np.array(image)

    result = reader.readtext(
        img,
        detail=0,
        paragraph=False
    )

    return "\n".join(result)
