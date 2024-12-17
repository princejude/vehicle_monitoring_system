from paddleocr import PaddleOCR, draw_ocr
from PIL import Image
import numpy as np
import re
import logging

#logging.getLogger().setLevel(logging.ERROR)  # Set to WARNING or ERROR to reduce verbosity

# Initialize PaddleOCR with detection and recognition enabled
ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False, use_gpu=False)

# Function to filter and clean text
def filter_and_clean_text(text):
    # Step 1: Match strings containing only A-Z, 0-9, and -
    valid_pattern = re.compile(r'^[A-Z0-9-]+$')
    if not valid_pattern.match(text):
        return None  # Return None if the string doesn't match

    # Step 2: Remove all non-alphanumeric characters and spaces
    clean_text = re.sub(r'[^\w]', '', text)  # Removes invalid characters
    return clean_text

# Path to the image
img_path = '/home/pi/Pictures/NigPics/paddleOCRtest.png'

# Perform OCR (enable text detection by default)
result = ocr.ocr(img_path, det=True, cls=True)

# Process and display results
if result:
    for idx in range(len(result)):
        res = result[idx]
        filtered_results = []  # Store filtered and cleaned results

        for line in res:
            raw_text = line[1][0]  # Extract the detected text
            cleaned_text = filter_and_clean_text(raw_text)  # Filter and clean text
            
            if cleaned_text:  # If valid, add it to filtered results
                line[1] = (cleaned_text, line[1][1])  # Update the cleaned text in the result
                filtered_results.append(line)
                print(f"Detected: {raw_text} | Cleaned: {cleaned_text}")

    # Extract and draw OCR results
    result = filtered_results  # Use filtered results
    image = Image.open(img_path).convert('RGB')

    # Extract information for visualization
    boxes = [line[0] for line in result if isinstance(line[0], list)]
    txts = [line[1][0] for line in result if len(line) > 1]
    scores = [line[1][1] for line in result if len(line) > 1]

    # Draw OCR results
    im_show = draw_ocr(
        image, boxes, txts, scores, font_path='/home/pi/Documents/PaddleOCR/doc/fonts/simfang.ttf'
    )

    # Convert NumPy array to PIL Image for display
    im_show = Image.fromarray(np.uint8(im_show))
    im_show.show()  # Display the image
    # im_show.save('result.jpg')  # Save the result image (optional)
else:
    print("No text detected in the image.")
