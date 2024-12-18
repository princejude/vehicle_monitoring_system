Road Vehicle Recognition and Classification System

Project Description

The Road Vehicle Recognition and Classification System is designed to enhance road safety monitoring by recognizing and classifying vehicles using Artificial Intelligent (AI), ultrasonic sensors, and a boom barrier control system. The project integrates ANPR (Automatic Number Plate Recognition) for vehicle identification, a vehicle classification system for categorizing vehicles, and notification system for monitoring and security alerts.

How the system works:

When a vehicle approaches the system, it will perform these actions in the following steps:

Step 1 - Detect vehicle using ultrasonic sensor.

Step 2 - Capture the vehicle's image with Pi camera module.

Step 3 - Extract the plate number from the image using PaddleOCR.

Step 4 - Check if the plate number is in database, if not in database, close the boom barrier and warn driver to go and register his/her vehicle. The driver will contact the admin to manually register his/her vehicle to the system through a registration form in the web portal.

Step 5 - If it is already registered in the database, check if it is marked as stolen in the status column of the vehicles’ table in the database, if it is stolen, close the boom barrier and send notification alert with the stolen vehicle’s details and location to security personnel.

Step 6 - If it is not stolen, classify the vehicle, if it is truck, check time, if it is peak period, close the boom barrier otherwise open the boom barrier.

Step 7. If it is not truck, open the boom barrier.

 
Project Features

1.	Vehicle Detection and Classification
   
    •	Ultrasonic sensor detects approaching vehicles.

    •	YOLOv8 is used to classify vehicles into categories: car, truck, bus, and motorbike.

2.	Automatic Number Plate Recognition (ANPR)

    •	PaddleOCR extracts the vehicle's plate number for identification.

3.	SQLite and SQLAlchemy is used for the vehicles Database Management.

4.	Security and Stolen Vehicle Monitoring

    •	If your vehicle is stolen, just call an admin and give him your plate number, he will log into the web portal, search for your vehicle details in the database, mark it as “STOLEN”. 

    •	If a vehicle is marked as stolen, once it approaches our system, the boom barrier stays closed, and an alert notification is sent to a security contact (e.g., WhatsApp/SMS).

5.	Time-Based Vehicle Restriction

    •	Trucks are restricted from passing during peak hours (7:00 AM - 7:00 PM).

6.	Web Portal

    •	Admin can manage the database of registered vehicles.

    •	Features include: Add, Edit, Delete, and Search for vehicles.

7.	Boom Barrier Control

    •	A servo motor controls the boom barrier based on the status, vehicle classification and time of the day.

8.	GPS Integration

    •	NEO-6M GPS module provides the system's location for alerts.

10.	Real-Time Alerts

    •	Notifications (WhatsApp/SMS) are sent for stolen vehicle detections, including location details.


 Hardware Used
 
Below are the hardware components used in the project:

Component 	Description

Raspberry Pi 4B, 4GB RAM - Main processing unit 

Ultrasonic Sensor (HC-SR04) -	Detects vehicle presence 

Camera Module - Captures images for ANPR and YOLO 

Servo Motor - Controls boom barrier 
 
NEO-6M GPS Module - Provides location details 

Power Supply - Powers all components 

Perf Board & Jumper Wires - For connections 

 
Software Setup

1. Software and Libraries

•	Operating System: Raspberry Pi OS, 64-bit, Bookworm.

•	Programming Language: Python 3.11

•	Flask: For the web portal.

•	PaddleOCR: For ANPR (license plate recognition).

•	YOLOv8 (COCO Dataset): For vehicle classification.

•	Twilio API: For WhatsApp/SMS alerts.

•	SQLAlchemy & SQLite: Database management.

•	Pi Camera: For camera operations.


2. Installation Instructions

Step 1: Clone the Repository

git clone https://github.com/princejude/vehicle_monitoring_system.git

cd vehicle_monitoring_system


Step 2: Set Up the Environment

•	Create a virtual environment and install dependencies:

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt


Step 3: Configure Sensitive Data

•	Create a .env file in the project root:

SECRET_KEY=your_secret_key  

TWILIO_SID=your_twilio_sid  

TWILIO_AUTH_TOKEN=your_auth_token  

SECURITY_CONTACT=your_security_contact_number  

GPS_MODULE_PORT=/dev/serial0  

Step 4: Run the Application

Start the Flask app and monitor the vehicle workflow:

python app/main.py


 Achievements So Far 
1.	Vehicle Detection & Classification: Successfully implemented vehicle detection and YOLO-based classification. 
2.	Automatic Number Plate Recognition (ANPR): PaddleOCR extracts vehicle plate numbers.
3.	Used Regular Expression (Regex) to identify ONLY Nigerian Plate Numbers.
4.	Database Management: Completed vehicle data management with Add, Edit, Delete, and Search functionalities.
5.	Boom Barrier Integration: Servo motor controls barrier based on vehicle type and time of day.
6.	Real-Time Notifications: Implemented Twilio-based alerts for stolen vehicle detection.
7.	Have Added real-time monitoring dashboard for vehicles.
 

 Remaining Tasks
1.	Tracking Stolen Vehicle:
•	GPS Location Integration: NEO-6M GPS module integration for location tracking, not done yet, because since the system is not mobile, I may remove the GPS module and get the system’s location, then include it in the code.
2.	Testing and Optimization:
•	Test the system under real-world conditions.
•	Optimize YOLOv8 and PaddleOCR for Raspberry Pi performance.
3.	Project Report:
•	Finalize the hardware, software, and performance documentation.
•	Add visualizations (e.g., flow diagrams, screenshots).
4.	Integration with Android App (Optional):
o	Provide Android app notifications for added accessibility.


 Contact 
For questions or further assistance, feel free to reach out:
•	Name: Ozioko Jude
•	Email: princejude@gmail.com
•	GitHub: @princejude


License
This project is open-source and licensed under the MIT License.


⭐ Support the Project
If you find this project useful, give it a ⭐ on GitHub to show your support!
 
