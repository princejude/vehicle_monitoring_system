from app.extensions import db
from app.models.user import User
from app import create_app

# Initialize the Flask app context
app = create_app()

with app.app_context():
    # Check if admin user already exists
    admin_user = User.query.filter_by(username='admin').first()

    if not admin_user:
        # Create admin user
        admin_user = User(
            username='admin',
            email='admin@example.com',
            is_admin=True,
            role='admin'
        )
        
        # Set a secure password for the admin
        admin_user.set_password('admin123')  # Replace 'admin123' with a strong password
        
        # Add the user to the database session and commit
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created successfully.")
    else:
        print("Admin user already exists.")
