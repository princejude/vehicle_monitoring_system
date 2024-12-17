"""
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
"""
from dotenv import load_dotenv
from app.utils.email_notification import send_email

load_dotenv()

send_email(
    receiver_email="princejude@gmail.com",
    subject="Test Email @ Project",
    body="Welcome, This is a test email to verify SMTP configuration."
)
