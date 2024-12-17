from ultralytics import YOLO

# Load the YOLOv8 model (replace with the correct model path)
model = YOLO('yolov8n.pt')

def classify_vehicle(image_path):
    """
    Classifies the vehicle in the provided image.

    Args:
        image_path (str): Path to the image to be classified.

    Returns:
        str: Classified vehicle type (e.g., 'car', 'truck').
    """
    from ultralytics import YOLO

    # Load the YOLO model
    model = YOLO("yolov8n.pt")  # Replace with your model path

    # Run YOLO model on the image
    results = model(image_path)

    # Check if results is a list and extract vehicle type
    if isinstance(results, list):
        for result in results:
            for box in result.boxes:  # Access detected boxes
                label = result.names[int(box.cls)]  # Map class index to label
                if label in ['car', 'truck', 'bus', 'motorbike']:
                    print(f"Detected: {label}")
                    return label
    else:
        print("Warning: Unrecognized results format from YOLO model.")

    return "unknown"
