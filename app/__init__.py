from flask import Flask, send_from_directory
from app.extensions import db, migrate, login_manager, csrf
import os


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')  # Load configuration

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Login configuration
    login_manager.login_view = 'auth_bp.login'
    login_manager.login_message = 'Please log in to access this page.'

    # Import User model and configure user_loader
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
 
    # Import and register blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.home_routes import home_bp
    from app.routes.vehicle_routes import vehicle_bp
    from app.routes.notify_routes import notify_bp
    from app.routes.log_routes import log_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(vehicle_bp, url_prefix='/vehicle')
    app.register_blueprint(notify_bp, url_prefix='/notify')
    app.register_blueprint(log_bp, url_prefix='/logs')  # Register only once

    # Serve processed images from a directory
    @app.route('/images/<path:filename>')
    def serve_images(filename):
        return send_from_directory('/home/pi/Pictures/NigPics', filename)

    # Ensure tables exist (development mode only)
    if app.config.get('ENV') == 'development':  # Check if environment is 'development'
        print("Running in development mode")
        with app.app_context():
            from app.models import Vehicle, VehicleLog, SystemLog
            db.create_all()

    return app


# Expose the Flask app instance
app = create_app()
