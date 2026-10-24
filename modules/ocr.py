import easyocr
import numpy as np

reader = easyocr.Reader(
    ['id', 'en'],
    gpu=False
)

def scan_text(image):

    img = np.array(image)

    result = reader.readtext(
        img,
        detail=0,
        paragraph=True
    )

    return "\n".join(result)
