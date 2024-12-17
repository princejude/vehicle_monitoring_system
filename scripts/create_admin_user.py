from app import create_app
from app.extensions import db
from app.models.user import User

def create_admin_user():
    # Create the Flask app instance
    app = create_app()

    # Use the application context for database operations
    with app.app_context():
        # Check if an admin user already exists
        existing_admin = User.query.filter_by(username='admin').first()
        if existing_admin:
            print("Admin user already exists.")
        else:
            # Create a new admin user
            admin = User(
                username='admin',
                email='admin@example.com',
                password_hash='hashed_password',  # Replace with a hashed password
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully.")

if __name__ == "__main__":
    create_admin_user()
