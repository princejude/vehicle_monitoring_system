import RPi.GPIO as GPIO
import time

# GPIO pin setup
SERVO_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(SERVO_PIN, GPIO.OUT)
servo = GPIO.PWM(SERVO_PIN, 50)  # 50Hz pulse for servo motor
servo.start(0)

def open_boom_barrier():
    """
    Opens the boom barrier using a servo motor.
    """
    print("Opening boom barrier...")
    servo.ChangeDutyCycle(7.5)  # Adjust as needed for your servo motor
    time.sleep(1)
    servo.ChangeDutyCycle(0)

def close_boom_barrier():
    """
    Closes the boom barrier using a servo motor.
    """
    print("Closing boom barrier...")
    servo.ChangeDutyCycle(2.5)  # Adjust as needed for your servo motor
    time.sleep(1)
    servo.ChangeDutyCycle(0)

# Cleanup GPIO on program exit
def cleanup():
    servo.stop()
    GPIO.cleanup()

import atexit
atexit.register(cleanup)
