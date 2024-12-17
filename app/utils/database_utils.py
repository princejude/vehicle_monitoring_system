from app.extensions import db
from app.models import Vehicle, VehicleLog, SystemLog


def log_event(event, details=None):
    """
    Log an event to the Logs table.
    """
    log_entry = Logs(event=event, details=details)
    db.session.add(log_entry)
    db.session.commit()

def search_vehicle_database(plate_number):
    """Search for vehicle details in the database by plate number."""
    with app.app_context():  # Ensure the app context is active
        vehicle = Vehicle.query.filter_by(plate_number=plate_number).first()
        return vehicle
