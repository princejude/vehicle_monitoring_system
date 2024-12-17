from app import create_app, db  # Import the factory function
from app.database import get_vehicle_data

# Create a new app instance
app = create_app()

# Use the application context to access the database
with app.app_context():
    plate_number = "LEM446AA"
    vehicle = get_vehicle_data(plate_number)
    if vehicle:
        print(f"Vehicle found: Plate Number: {vehicle.plate_number}, "
              f"Owner: {vehicle.owner_name}, Type: {vehicle.vehicle_type}")
    else:
        print("Vehicle not found.")
