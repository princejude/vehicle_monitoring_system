from app.extensions import db
from datetime import datetime

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plate_number = db.Column(db.String(10), unique=True, nullable=False)
    vehicle_type = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(50), nullable=False)  # "Normal" or "Stolen"
    owner_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    date_added = db.Column(db.Date, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Vehicle {self.plate_number} - {self.status}>'
