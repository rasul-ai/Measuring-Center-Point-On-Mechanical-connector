import cv2
import os
import csv

import joblib
import numpy as np
import pandas as pd

from ultralytics import YOLO
from error_diff import calc_diff


# Load the saved models and scaler
model_x = joblib.load('./models/model_x.joblib')
model_y = joblib.load('./models/model_y.joblib')
scaler = joblib.load('./models/scaler.joblib')


# Step 1: Define paths
model_path = './models/best.pt'  # Path to trained YOLOv8 model
image_path = './sample/conv_e_2.png'  # Path to the test image
output_folder = './results'  # Folder to save results
measured_data_folder = './measured_data'
csv_file_path = os.path.join(output_folder, os.path.splitext(os.path.basename(image_path))[0] + '.csv')
measured_data_path = os.path.join(measured_data_folder, os.path.splitext(os.path.basename(image_path))[0] + '.csv')

# Step 2: Load the trained YOLO model
model = YOLO(model_path)

# Step 3: Predict and save results
results = model.predict(
    source=image_path,  # Path to test image
    save_txt=True,  # Save predictions as .txt
    save=False,  # Skip saving annotated images automatically
    conf=0.5  # Confidence threshold
)



def correct_predictions(predicted_x, predicted_y):
    """
    Adjusts predicted_x and predicted_y so that the resulting x_diff and y_diff
    are within the range [-1, 1] using pre-trained regression models.
    """
    # Normalize the input
    inputs = scaler.transform([[predicted_x, predicted_y]])
    
    # Predict corrections
    x_correction = model_x.predict(inputs)[0]
    y_correction = model_y.predict(inputs)[0]
    
    # Apply corrections
    corrected_x = predicted_x - x_correction
    corrected_y = predicted_y - y_correction
    
    return corrected_x, corrected_y


# Step 4: Load the prediction `.txt` file
# YOLO saves `.txt` in the `runs/predict/` directory
prediction_folder = results[0].save_dir
txt_file_path = os.path.join(
    prediction_folder, 'labels', os.path.splitext(os.path.basename(image_path))[0] + '.txt'
)

if not os.path.exists(txt_file_path):
    raise FileNotFoundError(f"No prediction file found at {txt_file_path}")

# Step 5: Calculate centers and save to CSV
image = cv2.imread(image_path)
height, width, _ = image.shape

bounding_box_centers = []
with open(txt_file_path, 'r') as f:
    lines = f.readlines()
    for line in lines:
        # YOLO format: class_id x_center y_center width height
        class_id, x_center, y_center, box_width, box_height = map(float, line.split())

        # Calculate absolute coordinates of the center
        abs_x_center = int(x_center * width)
        abs_y_center = int((y_center) * height)

        # Saved format in 990*990 resolution
        center_x = x_center * 990
        center_y = 990 - (y_center * 990)   # Changed the y coordinates
        
        corrected_x, corrected_y = correct_predictions(center_x, center_y)
        

        bounding_box_centers.append((corrected_x, corrected_y))

        # Calculate absolute bounding box coordinates
        abs_width = int(box_width * width)
        abs_height = int(box_height * height)
        x1 = int(abs_x_center - abs_width / 2)
        y1 = int(abs_y_center - abs_height / 2)
        x2 = int(abs_x_center + abs_width / 2)
        y2 = int(abs_y_center + abs_height / 2)

        # Draw bounding box
        cv2.rectangle(image, (x1, y2), (x2, y1), (0, 255, 0), 2)  # Adjust y for lower-left origin

        # Draw center
        cv2.circle(image, (abs_x_center, abs_y_center), 5, (0, 0, 255), -1)  # Red for center

        # Add text for center coordinates
        center_text = f"({corrected_x:.2f}, {corrected_y:.2f})"
        cv2.putText(image, center_text, (abs_x_center + 10, abs_y_center + 20), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 5)

# Save centers to CSV
os.makedirs(output_folder, exist_ok=True)
with open(csv_file_path, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Center_X', 'Center_Y'])  # Header
    csvwriter.writerows(bounding_box_centers)

# Save annotated image
annotated_image_path = os.path.join(output_folder, os.path.basename(image_path))
cv2.imwrite(annotated_image_path, image)

# Load the dataset from the CSV file
# Replace 'input.csv' with the path to your CSV file
predicted_data = pd.read_csv(csv_file_path)
measured_data = pd.read_csv(measured_data_path)

error_diff = calc_diff(predicted_data, measured_data)
# print(type(error_diff))

# Save the final DataFrame to a CSV file
error_path = os.path.join(output_folder, os.path.splitext(os.path.basename(image_path))[0] + 'error_diff.csv')
error_diff.to_csv(error_path, index=False)


# Step 6: Print summary
print(f"Annotated image saved at: {annotated_image_path}")
print(f"Bounding box centers saved in CSV at: {csv_file_path}")
print(f"Error difference saved in CSV at: {error_path}")