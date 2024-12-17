from app.models import Vehicle

def get_vehicle_data(plate_number):
    """
    Retrieve vehicle and owner data from the database based on the plate number.
    """
    vehicle = Vehicle.query.filter_by(plate_number=plate_number).first()
    return vehicle
