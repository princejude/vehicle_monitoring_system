from app.utils.gps_location import get_gps_location

if __name__ == "__main__":
    location = get_gps_location()
    if location:
        print(f"Current Location: Latitude={location['latitude']}, Longitude={location['longitude']}")
    else:
        print("Failed to retrieve GPS location.")
