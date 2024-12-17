from app.utils.gps_location import send_notification

test_vehicle_data = {
    "plate_number": "ABJ123KB",
    "type": "Car",
    "owner_name": "John Bull",
    "phone": "08034567890",
    "address": "12 Main St, Kaduna"
}
receiver_email = "princejude@gmail.com"
send_notification(receiver_email, test_vehicle_data)
