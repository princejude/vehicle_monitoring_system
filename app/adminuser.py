from app import create_app, db
from app.models import User

# Create an application instance
app = create_app()

# Activate the application context
with app.app_context():
    # Create an admin user
    admin = User(username='admin', email='princejude@gmail.com', role='admin')
    admin.set_password('admin042')
    
    # Add the user to the database
    db.session.add(admin)
    db.session.commit()

print("Admin user added successfully.")
