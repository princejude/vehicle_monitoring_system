from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db  # Ensure db is imported
from app.forms import NotifyStolenForm
from app.models import Vehicle
from app.utils.notification_utils import send_notification

notify_bp = Blueprint('notify_bp', __name__, template_folder='templates')

@notify_bp.route('/stolen', methods=['GET', 'POST'])
def notify_stolen():
    form = NotifyStolenForm()

    if request.method == 'POST' and form.validate_on_submit():
        plate_number = form.plate_number.data.strip()
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
