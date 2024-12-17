import RPi.GPIO as GPIO
import time
from picamera2 import Picamera2
from PIL import Image

# Ultrasonic sensor pins
TRIG_PIN = 18
ECHO_PIN = 24

# Setup function for ultrasonic sensor
def setup_sensor():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)

# Detect vehicle using ultrasonic sensor
def detect_vehicle():
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    while GPIO.input(ECHO_PIN) == 0:
        start_time = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        end_time = time.time()

    duration = end_time - start_time
    distance = (duration * 34300) / 2  # Distance in cm
    return distance < 50  # Trigger for vehicles within 50 cm

# Capture image using Picamera2
def capture_image(output_path):
    try:
        picam2 = Picamera2()
        config = picam2.create_still_configuration()
        picam2.configure(config)
        picam2.start()
        time.sleep(2)  # Warm-up time
        image = picam2.capture_array()  # Capture as a NumPy array
        picam2.stop()

        # Convert to PIL Image and save
        pil_image = Image.fromarray(image)
        pil_image.save(output_path)
    except Exception as e:
        raise RuntimeError(f"Failed to capture image: {e}")

# Test the sensor.py module
if __name__ == "__main__":
    setup_sensor()
    print("Testing Ultrasonic Sensor:")
    vehicle_detected = detect_vehicle()
    print(f"Vehicle Detected: {vehicle_detected}")

    if vehicle_detected:
        print("Capturing Image...")
        capture_image("test_image.jpg")
        print("Image Captured and Saved as test_image.jpg")
