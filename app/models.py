from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, DateTime, func
from app.db import Base

class VehicleLog(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True)
    plate_number = Column(String, nullable=False)
    vehicle_type = Column(String, nullable=False)
    action_taken = Column(String, nullable=False)
    timestamp = Column(DateTime, default=func.now())
    image_path = Column(String, nullable=False)

    def __repr__(self):		
        return f"<VehicleLog {self.plate_number}>"
