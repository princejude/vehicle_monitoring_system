from app import create_app, db

app = create_app()
print(f"Using database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

with app.app_context():
    try:
        db.create_all()
        print("Database and tables created successfully!")
    except Exception as e:
        print(f"Error occurred: {e}")
