from app import db

class VehicleLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_plate = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<VehicleLog {self.vehicle_plate} - {self.timestamp}>'
