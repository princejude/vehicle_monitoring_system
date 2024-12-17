from flask import (
    Blueprint, render_template, request, redirect, url_for, flash
)
from flask_login import login_user, logout_user, login_required
from app.models import User
from app.forms import LoginForm, RegistrationForm  # Import forms
from werkzeug.security import check_password_hash, generate_password_hash
from app.extensions import db

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Instantiate the LoginForm

    if form.validate_on_submit():  # Validates CSRF and form fields
        username = form.username.data
        password = form.password.data

        # Fetch user from the database
        user = User.query.filter_by(username=username).first()

        # Check if the user exists and the password matches
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Logged in successfully!', 'success')

            # Redirect to the next page or home
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('vehicle_bp.dashboard'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('auth/login.html', title='Login', form=form)  # Pass the form to the template

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()  # Use RegistrationForm
    if form.validate_on_submit():  # Automatically validates CSRF and other fields
        username = form.username.data
        email = form.email.data
        password = form.password.data

        hashed_password = generate_password_hash(password, method='scrypt')

        # Create a new user
        new_user = User(username=username, email=email, password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('auth_bp.login'))  # Corrected URL
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')
    
    return render_template('auth/register.html', form=form)  # Pass the form object

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('auth_bp.login'))
