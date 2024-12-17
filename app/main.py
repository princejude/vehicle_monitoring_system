import os
import time
from threading import Thread
from datetime import datetime
import sqlite3

from app import create_app
from app.utils.globals import processed_images, event_logs
from app.utils.time_check import is_peak_time
from app.utils.vehicle_classifier import classify_vehicle
from app.utils.barrier_control import open_boom_barrier, close_boom_barrier
from app.utils.notification_utils import send_notification

# Configurable settings
DATABASE_PATH = os.getenv("DATABASE_PATH", "/home/pi/road_safety/road_safety.db")
PROCESSED_IMAGE_DIR = os.getenv("PROCESSED_IMAGE_DIR", "/home/pi/road_safety/processed_images/")
IMAGE_DIR = os.getenv("IMAGE_DIR", "/home/pi/Pictures/NigPics/")
STOP_THREAD = False  # Flag to control the workflow thread

# Initialize Flask app
app = create_app()


# Utility functions
def get_db_connection():
    """
    Establishes a connection to the SQLite database.
    """
    return sqlite3.connect(DATABASE_PATH)


def log_event(event, image_path=None):
    """
    Log processed events with timestamps and optional image paths.
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = {"timestamp": timestamp, "event": event, "image_path": image_path}
    event_logs.append(log_entry)
    if image_path:
        processed_images.append(image_path)
    print(f"[LOG] {log_entry}")  # Optional: Print logs to the console


def search_vehicle_by_plate(plate_number):
    """
    Retrieve vehicle data by plate number from the database.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT plate_number, status FROM vehicle WHERE plate_number = ?", (plate_number,))
        return cursor.fetchone()


def save_processed_image(img_path, plate_number):
    """
    Save the processed image to the processed_images directory with a unique name.
    """
    if not os.path.exists(PROCESSED_IMAGE_DIR):
        os.makedirs(PROCESSED_IMAGE_DIR)

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    file_name = f"{plate_number}_{timestamp}.png"
    save_path = os.path.join(PROCESSED_IMAGE_DIR, file_name)
    os.rename(img_path, save_path)
    return save_path


# Main workflow
def main_workflow():
    """
    Main workflow to detect vehicles, verify them, classify, and control the boom barrier.
    """
    global STOP_THREAD
    while not STOP_THREAD:
        img_path = os.path.join(IMAGE_DIR, "pic5.png")

        # Wait for the image file to exist
        if not os.path.exists(img_path):
            time.sleep(5)
            continue

        log_event("Processing vehicle image...", img_path)

        # Step 1: Extract vehicle plate (replace with real ANPR call)
        detected_plate = "LEM446AA"
        log_event(f"Detected Plate Number: {detected_plate}")

        # Step 2: Search vehicle in the database
        vehicle_data = search_vehicle_by_plate(detected_plate)
        if not vehicle_data:
            log_event("Vehicle not found in database.", img_path)
            time.sleep(5)
            continue

        plate_number, status = vehicle_data
        log_event(f"Vehicle Found: Plate {plate_number}, Status: {status}")

        # Step 3: Handle stolen vehicles
        if status.lower() == "stolen":
            log_event("Vehicle is stolen. Closing boom barrier.", img_path)
            close_boom_barrier()
            send_notification(plate_number, location="System Location")
            save_processed_image(img_path, plate_number)
            time.sleep(5)
            continue

        # Step 4: Classify vehicle type
        vehicle_type = classify_vehicle(img_path)
        log_event(f"Vehicle Classified: {vehicle_type}")

        # Step 5: Enforce peak-hour rules
        if vehicle_type.lower() == "truck" and is_peak_time():
            log_event("Truck detected during peak hours. Closing boom barrier.", img_path)
            close_boom_barrier()
        else:
            log_event("Opening boom barrier.", img_path)
            open_boom_barrier()

        # Step 6: Save processed image
        save_processed_image(img_path, plate_number)
        time.sleep(5)


# Thread management
def start_workflow_thread():
    """
    Start the main workflow in a separate thread.
    """
    workflow_thread = Thread(target=main_workflow, daemon=True)
    workflow_thread.start()
    print("Workflow thread started.")


def stop_workflow():
    """
    Stop the workflow thread.
    """
    global STOP_THREAD
    STOP_THREAD = True
    print("Workflow thread stopped.")


# Entry point
if __name__ == "__main__":
    try:
        start_workflow_thread()
        app.run(debug=True, host = '0.0.0.0', port = 5000, use_reloader=False)
    except KeyboardInterrupt:
        stop_workflow()
