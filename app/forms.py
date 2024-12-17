from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField, TextAreaField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, Regexp, ValidationError, Email, EqualTo
from datetime import date
from app.models import Vehicle

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class VehicleForm(FlaskForm):
    id = HiddenField("ID")  # Hidden field for vehicle ID
    plate_number = StringField(
        'Plate Number',
        validators=[
            DataRequired(message="Plate number is required."),
            Length(max=9, message="Plate number cannot exceed 9 characters."),
            Regexp(r'^[A-Z0-9-]+$', message="Plate number must be alphanumeric.")
        ]
    )
    vehicle_type = SelectField(
        'Vehicle Type',
        choices=[
            ('', 'Select Vehicle Type'),
            ('car', 'Car'),
            ('truck', 'Truck'),
            ('bus', 'Bus'),
            ('motorbike', 'Motorbike')
        ],
        validators=[DataRequired(message="Please select a vehicle type.")]
    )
    status = SelectField(
        'Vehicle Status',
        choices=[
            ('', 'Select Status'),
            ('normal', 'Normal'),
            ('stolen', 'Stolen')
        ],
        validators=[DataRequired(message="Please select the vehicle status.")]
    )
    owner_name = StringField(
        "Owner's Name",
        validators=[
            DataRequired(message="Owner's name is required."),
            Length(max=20, message="Owner's name cannot exceed 20 characters.")
        ]
    )
    phone_number = StringField(
        "Owner's Phone Number",
        validators=[
            DataRequired(message="Owner's phone number is required."),
            Length(max=15, message="Phone number cannot exceed 15 characters."),
            Regexp(r'^\+?\d{10,15}$', message="Enter a valid phone number (10-15 digits).")
        ]
    )
    address = TextAreaField(
        "Owner's Address",
        validators=[
            DataRequired(message="Address is required."),
            Length(max=25, message="Address cannot exceed 25 characters.")
        ]
    )
    date_added = DateField(
        'Registration Date',
        format='%Y-%m-%d',
        default=date.today,
        validators=[DataRequired(message="Please provide a valid date (YYYY-MM-DD).")]
    )
    submit = SubmitField('Submit')

    def validate_plate_number(self, plate_number):
        existing_vehicle = Vehicle.query.filter_by(plate_number=plate_number.data).first()
        if existing_vehicle and existing_vehicle.id != int(self.id.data or 0):
            raise ValidationError("Plate number already exists. Please provide a unique plate number.")

class NotifyStolenForm(FlaskForm):
    plate_number = StringField(
        'Plate Number',
        validators=[
            DataRequired(message="Plate number is required."),
            Length(min=1, max=9, message="Plate number must be between 1 and 20 characters.")
        ]
    )
    submit = SubmitField('Report Stolen Vehicle')

class SearchVehicleForm(FlaskForm):
    search_query = StringField(
        'Search by Plate Number or Owner\'s Name:',
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter plate number or owner's name"}
    )
    submit = SubmitField('Search')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('admin', 'Admin'), ('user', 'User')], validators=[DataRequired()])
    submit = SubmitField('Register')
    
class CreateUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    role = SelectField('Role', choices=[('Admin', 'Admin'), ('User', 'User')], validators=[DataRequired()])
    submit = SubmitField('Create User')
    
