
#classification and recognition

from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang='en') # need to run only once to load model into memory

#img_path = '/home/pi/Pictures/overseas/saudi_car_plate.jpg'
img_path = '/home/pi/Pictures/images/004.jpg'


result = ocr.ocr(img_path, det=False, cls=True)
for line in result:
    print(line)


