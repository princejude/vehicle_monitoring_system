import os

class Config:
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'jdbd-rjdb-cbvj-qbwg')
    
    # General configuration
    ENV = 'development'  # Set 'development' or 'production' based on your environment
    DEBUG = True  # Enable debug mode
    
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', f"sqlite:///{os.path.abspath('road_safety.db')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    # Notification settings
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
    
    # Location API key (if applicable)
    LOCATION_API_KEY = os.getenv('LOCATION_API_KEY')

