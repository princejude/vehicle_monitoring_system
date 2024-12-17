from app.models import Vehicle

def send_notification(vehicle, location):
    """Send a notification if the vehicle is reported as stolen."""
    message = (
        f"ALERT! A stolen vehicle has been detected.\n"
        f"Plate Number: {vehicle.plate_number}\n"
        f"Owner: {vehicle.owner_name}\n"
        f"Phone: {vehicle.phone_number}\n"
        f"Location: {location}\n"
    )
    print("Sending notification:")
    print(message)
    # Add integration for SMS or WhatsApp API here (e.g., Twilio, etc.)
