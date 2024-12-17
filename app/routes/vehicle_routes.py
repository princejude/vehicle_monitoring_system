# app/routes/vehicle_routes.py

from flask import Blueprint, render_template, redirect, url_for, flash, request, Response, jsonify
from app.forms import VehicleForm, NotifyStolenForm, SearchVehicleForm
from app.models import Vehicle
from app import db
from sqlalchemy import func
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.exc import SQLAlchemyError
from flask_login import login_required
from io import StringIO
import csv
from app.forms import VehicleForm
from app.utils.globals import processed_images, event_logs  # Import global variables

from app.utils.sensor import detect_vehicle, capture_image
from app.utils.anpr import extract_plate
from app.utils.vehicle_classifier import classify_vehicle
from app.utils.barrier_control import open_boom_barrier, close_boom_barrier
from app.utils.time_check import is_peak_time
from app.utils.notification_utils import send_notification

# Blueprint setup
vehicle_bp = Blueprint('vehicle_bp', __name__, url_prefix='/vehicles')

@vehicle_bp.route('/add_vehicle', methods=['GET', 'POST'])
@login_required
def add_vehicle():
    form = VehicleForm()

    if form.validate_on_submit():
        # Check for duplicate plate number
        existing_vehicle = Vehicle.query.filter_by(plate_number=form.plate_number.data).first()
        if existing_vehicle:
            flash('Vehicle with this plate number already exists!', 'danger')
            return render_template('vehicle/add_vehicle.html', form=form)

        try:
            # Save the new vehicle to the database
            new_vehicle = Vehicle(
                plate_number=form.plate_number.data.strip(),
                vehicle_type=form.vehicle_type.data,
                status=form.status.data,
                owner_name=form.owner_name.data.strip(),
                phone_number=form.phone_number.data.strip(),
                address=form.address.data.strip(),
                date_added=form.date_added.data
            )
            db.session.add(new_vehicle)
            db.session.commit()
            flash('Vehicle added successfully!', 'success')
            return redirect(url_for('vehicle_bp.view_vehicles'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while adding the vehicle. Please try again.', 'danger')
            print(f"Error: {e}")

    return render_template('vehicle/add_vehicle.html', form=form)

# View all vehicles with pagination
@vehicle_bp.route('/view', methods=['GET'])
def view_vehicles():
    try:
        # Pagination logic
        page = request.args.get('page', 1, type=int)
        per_page = 10
        vehicles = Vehicle.query.paginate(page=page, per_page=per_page)
        return render_template('vehicle/view_vehicles.html', vehicles=vehicles)
    except SQLAlchemyError as e:
        flash(f"An error occurred: {str(e)}", 'danger')
        return redirect(url_for('main.index'))

@vehicle_bp.route("/vehicles", methods=["GET"])
def get_vehicles():
    # Example route that uses the global variables
    return jsonify({
        "processed_images": processed_images,
        "event_logs": event_logs
    })
    
# Delete a vehicle
@vehicle_bp.route('/delete/<int:vehicle_id>', methods=['POST'])
@login_required
def delete_vehicle(vehicle_id):
    try:
        vehicle = Vehicle.query.get_or_404(vehicle_id)
        db.session.delete(vehicle)
        db.session.commit()
        flash(f"Vehicle {vehicle.plate_number} deleted successfully.", 'success')
    except SQLAlchemyError as e:
        flash(f"Error deleting vehicle: {str(e)}", 'danger')
        db.session.rollback()
    return redirect(url_for('vehicle_bp.view_vehicles'))
    
# Edit a vehicle (placeholder; implement as needed)
@vehicle_bp.route('/edit_vehicle/<int:vehicle_id>', methods=['GET', 'POST'])
@login_required
def edit_vehicle(vehicle_id):
    # Fetch the existing vehicle record
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    form = VehicleForm(obj=vehicle)  # Preload form with existing data
    
    # Populate the hidden `id` field with the vehicle's ID
    form.id.data = vehicle.id

    if form.validate_on_submit():  # Handle POST request
        # Update vehicle details
        vehicle.plate_number = form.plate_number.data
        vehicle.vehicle_type = form.vehicle_type.data
        vehicle.status = form.status.data
        vehicle.owner_name = form.owner_name.data
        vehicle.phone_number = form.phone_number.data
        vehicle.address = form.address.data
        vehicle.date_added = form.date_added.data
        
        # Save changes to the database
        try:
            db.session.commit()
            flash('Vehicle details updated successfully!', 'success')
            return redirect(url_for('vehicle_bp.view_vehicles', vehicle_id=vehicle.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating vehicle: {str(e)}', 'danger')
    
    # Handle GET request (or if form validation fails)
    return render_template('vehicle/edit_vehicle.html', form=form, vehicle=vehicle)
    
@vehicle_bp.route('/search', methods=['GET', 'POST'])
def search_vehicle():
    form = SearchVehicleForm()
    vehicle = None
    searched = False

    if form.validate_on_submit():
        search_query = form.search_query.data.strip()
        # Perform the search logic here
        vehicle = Vehicle.query.filter(
            (Vehicle.plate_number.ilike(f"%{search_query}%")) |
            (Vehicle.owner_name.ilike(f"%{search_query}%"))
        ).first()
        searched = True

    return render_template(
        'vehicle/search_vehicle.html',
        form=form,
        vehicle=vehicle,
        searched=searched
    )
    
@vehicle_bp.route('/notify/stolen', methods=['GET', 'POST'])
def notify_stolen():
    form = NotifyStolenForm()

    if request.method == 'POST' and form.validate_on_submit():
        plate_number = form.plate_number.data
        vehicle = Vehicle.query.filter_by(plate_number=plate_number).first()

        if not vehicle:
            flash('Vehicle not found. Please check the plate number.', 'danger')
        elif vehicle.status == 'stolen':
            flash('This vehicle is already reported as stolen.', 'info')
        else:
            vehicle.status = 'stolen'
            db.session.commit()
            flash(f'Vehicle {plate_number} has been marked as stolen.', 'success')
            # Add notification logic here
            send_notification(vehicle, location="Current System Location")
        return redirect(url_for('vehicle_bp.view_vehicles'))

    return render_template('notify_stolen.html', form=form)
    
@vehicle_bp.route('/dashboard')
def dashboard():
    total_vehicles = Vehicle.query.count()
    stolen_vehicles = Vehicle.query.filter_by(status="stolen").count()
    total_cars = Vehicle.query.filter_by(vehicle_type="car").count()
    total_trucks = Vehicle.query.filter_by(vehicle_type="truck").count()
    total_motorbikes = Vehicle.query.filter_by(vehicle_type="motorbike").count()
    total_buses = Vehicle.query.filter_by(vehicle_type="bus").count()

    return render_template(
        'vehicle/dashboard.html',
        total_vehicles=total_vehicles,
        stolen_vehicles=stolen_vehicles,
        total_cars=total_cars,
        total_trucks=total_trucks,
        total_motorbikes=total_motorbikes,
        total_buses=total_buses
    )

@vehicle_bp.route('/generate_report/<filter>', methods=['GET'])
def generate_report(filter):
    # Fetch vehicles based on filter
    if filter == 'all':
        vehicles = Vehicle.query.all()
    elif filter == 'stolen':
        vehicles = Vehicle.query.filter_by(status='stolen').all()
    else:
        vehicles = Vehicle.query.filter_by(vehicle_type=filter).all()

    # Create a CSV file in memory
    output = StringIO()
    writer = csv.writer(output)
    
    # Write CSV header
    writer.writerow(['Plate Number', 'Type', 'Status', 'Owner Name', 'Phone Number', 'Address', 'Date Added'])

    # Write CSV rows
    for vehicle in vehicles:
        writer.writerow([
            vehicle.plate_number,
            vehicle.vehicle_type,
            vehicle.status,
            vehicle.owner_name,
            vehicle.phone_number,
            vehicle.address,
            vehicle.date_added
        ])

    # Prepare the response
    output.seek(0)
    response = Response(output, mimetype='text/csv')
    response.headers['Content-Disposition'] = f'attachment; filename={filter}_vehicles.csv'
    return response

@vehicle_bp.route('/process_anpr', methods=['POST'])
def process_anpr():
    """
    Process ANPR to validate and check the database for the detected plate number.
    """
    # Path to the uploaded image (e.g., from a POST request or captured image path)
    img_path = request.json.get('img_path')

    if not img_path:
        return jsonify({'error': 'Image path is required.'}), 400

    # Perform ANPR
    plates = perform_anpr(img_path)

    if not plates:
        return jsonify({'message': 'No valid plates detected.'}), 404

    # Check each validated plate against the database
    for plate, confidence in plates:
        vehicle = Vehicle.query.filter_by(plate_number=plate).first()

        if vehicle:
            return jsonify({
                'plate_number': plate,
                'status': vehicle.status,
                'vehicle_type': vehicle.vehicle_type,
                'message': 'Plate found in the database.',
                'confidence': confidence
            })

    return jsonify({'message': 'Plate not found in the database.', 'plates': plates})

@vehicle_bp.route('/process_vehicle', methods=['POST'])
def process_vehicle():
    if detect_vehicle():
        image_path = "/path/to/captured_image.jpg"
        capture_image(image_path)
        
        plate_number = extract_plate(image_path)
        if not plate_number:
            return jsonify({"message": "Plate number could not be detected."}), 400
        
        vehicle = Vehicle.query.filter_by(plate_number=plate_number).first()
        if not vehicle:
            close_barrier()
            return jsonify({"message": "Vehicle not registered. Please register."}), 400
        
        vehicle_type = classify_vehicle(image_path)
        is_peak = is_peak_time()
        
        if vehicle.status == "Stolen":
            #send_notification(f"Stolen vehicle detected: {plate_number}", security_phone, is_stolen=True)
            close_barrier()
            return jsonify({"message": "Stolen vehicle detected. Authorities notified."}), 403

        if vehicle_type == "Truck" and is_peak:
            close_barrier()
            return jsonify({"message": "Truck not allowed during peak hours."}), 403
        
        open_barrier()
        return jsonify({"message": f"Welcome, {vehicle.owner_name}. Vehicle type: {vehicle_type}."}), 200

@vehicle_bp.route('/processed-images')
def view_processed_images():
    """
    Display the list of processed images on the web portal.
    """
    return render_template('processed_images.html', images=processed_images)

@vehicle_bp.route('/logs')
def view_logs():
    """
    Display event logs on the web portal.
    """
    return render_template('event_logs.html', logs=event_logs)

