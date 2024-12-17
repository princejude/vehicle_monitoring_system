from paddleocr import PaddleOCR, draw_ocr
from PIL import Image
import numpy as np
import re

# Initialize PaddleOCR with detection and recognition enabled
ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False, use_gpu=False)

# Function to validate Nigerian plate number format
def is_valid_nigerian_plate(text):
    """
    Validates if the text matches the Nigerian plate number format:
    - 2-3 leading alphabets (A-Z)
    - 2-3 digits in the middle (0-9)
    - 2-3 trailing alphabets (A-Z)
    No hyphens, spaces, or special characters.
    """
    # Regex pattern for Nigerian plate numbers
    pattern = re.compile(r'^[A-Z]{2,3}[0-9]{2,3}[A-Z]{2,3}$')
    return bool(pattern.match(text))

# Path to the image
img_path = '/home/pi/Pictures/NigPics/paddleOCRtest.png'

# Perform OCR on the image
result = ocr.ocr(img_path, det=True, cls=True)

# Process results and validate Nigerian plate numbers
if result:
    print("Processing detected text...")
    for idx in range(len(result)):
        res = result[idx]
        valid_results = []  # To store valid Nigerian plate numbers

        for line in res:
            raw_text = line[1][0]  # Extract the detected text
            
            # Clean text by removing non-alphanumeric characters
            cleaned_text = re.sub(r'[^\w]', '', raw_text)

            # Validate the cleaned text as a Nigerian plate number
            if is_valid_nigerian_plate(cleaned_text):
                valid_results.append((line[0], (cleaned_text, line[1][1])))  # Add valid plate to results
                print(f"Valid Nigerian Plate Detected: {cleaned_text}")
            else:
                print(f"Ignored: {raw_text} (Cleaned: {cleaned_text})")

    if valid_results:
        # Draw results for valid Nigerian plate numbers
        image = Image.open(img_path).convert('RGB')
        boxes = [line[0] for line in valid_results]
        texts = [line[1][0] for line in valid_results]
        scores = [line[1][1] for line in valid_results]

        # Visualize results with PaddleOCR's draw_ocr
        im_show = draw_ocr(
            image, boxes, texts, scores,
            font_path='/home/pi/Documents/PaddleOCR/doc/fonts/simfang.ttf'
        )

        # Convert the result to a displayable image
        im_show = Image.fromarray(np.uint8(im_show))
        im_show.show()  # Display the image
        # im_show.save('nigerian_plate_results.jpg')  # Optional: Save the result
    else:
        print("No valid Nigerian plate numbers detected.")
else:
    print("No text detected in the image.")
