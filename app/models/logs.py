from app import db
from datetime import datetime

class SystemLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    details = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<SystemLog {self.event}>"
