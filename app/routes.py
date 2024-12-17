#from app.extensions import db
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory
from app.models import User, Vehicle, VehicleLog, SystemLog
from app.forms import VehicleForm
from app.db import get_db_session

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/add-vehicle', methods=['GET', 'POST'])
def add_vehicle():
    form = VehicleForm()
    if form.validate_on_submit():
        # Create a new vehicle entry
        new_vehicle = Vehicle(
            plate_number=form.plate_number.data,
            vehicle_type=form.vehicle_type.data,
            status=form.status.data,
            owner_name=form.owner_name.data,
            phone_number=form.phone_number.data,
            address=form.address.data,
            date=form.date.data
        )
        db.session.add(new_vehicle)
        db.session.commit()
        flash('Vehicle added successfully!', 'success')
        return redirect(url_for('routes.index'))
    return render_template('add_vehicle.html', form=form)

@bp.route('/view-vehicles')
def view_vehicles():
    vehicles = Vehicle.query.all()
    return render_template('view_vehicles.html', vehicles=vehicles)

# Route to serve processed images
@bp.route('/processed_images/<filename>')
def processed_image(filename):
    return send_from_directory('/home/pi/road_safety/processed_images/', filename)

# Route to view logs
@bp.route('/logs')
def view_logs():
    session = get_db_session()
    logs = session.query(Logs).all()
    return render_template('logs.html', logs=logs)
