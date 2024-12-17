# app/utils/anpr.py
import re
import logging
from paddleocr import PaddleOCR


logging.getLogger().setLevel(logging.ERROR)  # Set to WARNING or ERROR to reduce verbosity

ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False, show_log=False)

def extract_plate(image_path):
    result = ocr.ocr(image_path)
    for line in result[0]:
        text, _ = line[1]
        text = re.sub(r'[^A-Z0-9]', '', text)
        if validate_plate_format(text):
            return text
    return None

def validate_plate_format(plate):
    """
    Validates the text format based on the following:
    - First 2-3 characters: Alphabets
    - Next 2-3 characters: Numbers
    - Remaining 2-3 characters: Alphabets (optional)
    - Maximum number of characters: 9.
    """
    pattern = r'^[A-Z]{2,3}[0-9]{2,3}[A-Z]{2,3}$'
    return bool(re.match(pattern, plate))
