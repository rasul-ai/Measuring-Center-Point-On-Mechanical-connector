from ultralytics import YOLO

# Load the YOLOv8 model (replace 'yolov8_model.pt' with your model file)
model = YOLO('./Bolt_nut_v2/train/weights/best.pt')

# Define the path to the image or video for inference
image_path = './Bolt_nut_v2/data/images/test'  # Replace with your image path

# Perform inference
results = model.predict(source=image_path, save=True, save_txt=True, conf=0.5)