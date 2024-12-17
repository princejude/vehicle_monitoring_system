import re
import logging
from paddleocr import PaddleOCR

# Suppress PaddleOCR logs
logging.getLogger().setLevel(logging.ERROR)

# Initialize PaddleOCR with required configurations
ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False, show_log=False)


def extract_plate(image_path):
    """
    Extracts Nigerian plate number from an image using PaddleOCR.

    Args:
        image_path (str): Path to the image containing the plate.

    Returns:
        str: The detected Nigerian plate number, or None if not found.
    """
    try:
        # Perform OCR on the image
        result = ocr.ocr(image_path, det=True, cls=True)

        if result:
            for line in result[0]:
                raw_text = line[1][0]  # Extract detected text
                cleaned_text = re.sub(r'[^\w]', '', raw_text)  # Clean non-alphanumeric characters

                # Validate as a Nigerian plate number
                if validate_plate_format(cleaned_text):
                    return cleaned_text  # Return the first valid plate detected
        return None  # No valid plate found
    except Exception as e:
        logging.error(f"Error during OCR: {e}")
        return None


def validate_plate_format(plate):
    """
    Validates if the text matches the Nigerian plate number format.

    Format:
        - First 2-3 characters: Alphabets
        - Next 2-3 characters: Digits
        - Last 2-3 characters: Alphabets
        - No spaces, hyphens, or special characters.

    Args:
        plate (str): The text to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    pattern = r'^[A-Z]{2,3}[0-9]{2,3}[A-Z]{2,3}$'
    return bool(re.match(pattern, plate))


def test_anpr(image_path):
    """
    Test function to validate the ANPR process on a given image.

    Args:
        image_path (str): Path to the image for testing.

    Returns:
        str: Valid Nigerian plate number or a failure message.
    """
    plate = extract_plate(image_path)
    if plate:
        print(f"Valid Nigerian Plate Detected: {plate}")
        return plate
    else:
        print("No valid Nigerian plate detected.")
        return "No valid plate detected."


if __name__ == "__main__":
    # Example usage and testing
    img_path = "/home/pi/Pictures/NigPics/paddleOCRtest.png"  # Update with your image path
    test_anpr(img_path)
