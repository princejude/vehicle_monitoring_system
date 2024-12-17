from paddleocr import PaddleOCR, draw_ocr
from PIL import Image
import numpy as np

# Initialize PaddleOCR with detection and recognition enabled
ocr = PaddleOCR(use_angle_cls=True, lang='en')

# Path to the image
img_path = '/home/pi/Pictures/NigPics/paddleOCRtest.png'

# Perform OCR (enable text detection by default)
result = ocr.ocr(img_path, det=True, cls=True)

# Process and display results
if result:
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            print(line)  # Print each line (bounding box, text, score)

    # Extract and draw OCR results
    result = result[0]  # Focus on the first result
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
