from flask import Blueprint, render_template
from datetime import datetime
from app import db


log_bp = Blueprint('log_bp', __name__)

# Temporary list for system event logs
system_logs = []


def log_system_event(description, severity="info"):
    """
    Log system events with a description and severity level.
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = {
        "timestamp": timestamp,
        "description": description,
        "severity": severity.lower(),  # "info", "warning", or "critical"
    }
    system_logs.append(log_entry)


@log_bp.route('/logs')
def view_vehicle_logs():
    """
    Route to view processed vehicle logs.
    """
    from app.models import VehicleLog  # Ensure you have the VehicleLog model
    # Query all vehicle logs from the database
    logs = VehicleLog.query.order_by(VehicleLog.timestamp.desc()).all()
    return render_template('logs.html', logs=logs)


@log_bp.route('/event_logs')
def view_event_logs():
    """
    Route to view system event logs.
    """
    return render_template('event_logs.html', event_logs=system_logs, current_year=datetime.now().year)
