import cv2
import os

def split_image_with_overlap(image_path, output_folder, overlap=0.05):
    # Read the image
    image = cv2.imread(image_path)
    height, width = image.shape[:2]
    overlap_x = int(width * overlap)
    overlap_y = int(height * overlap)
    mid_x = width // 2
    mid_y = height // 2
    
    # Split the image into four overlapping pieces
    top_left = image[:mid_y + overlap_y, :mid_x + overlap_x]
    top_right = image[:mid_y + overlap_y, mid_x - overlap_x:]
    bottom_left = image[mid_y - overlap_y:, :mid_x + overlap_x]
    bottom_right = image[mid_y - overlap_y:, mid_x - overlap_x:]
    
    # Get the base name of the image file
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    
    # Save the pieces with appropriate names
    cv2.imwrite(os.path.join(output_folder, f"{base_name}_top_left.png"), top_left)
    cv2.imwrite(os.path.join(output_folder, f"{base_name}_top_right.png"), top_right)
    cv2.imwrite(os.path.join(output_folder, f"{base_name}_bottom_left.png"), bottom_left)
    cv2.imwrite(os.path.join(output_folder, f"{base_name}_bottom_right.png"), bottom_right)
    
    return top_left, top_right, bottom_left, bottom_right, (overlap_x, overlap_y)

# Main code to process all images in a folder
input_folder = './Bolt_nut_v2/fullimg'
output_folder = './data'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(input_folder, filename)
        split_image_with_overlap(image_path, output_folder)
