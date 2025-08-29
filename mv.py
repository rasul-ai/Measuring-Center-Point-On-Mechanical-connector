import shutil
import os

# Define source and destination folders
source_folder = "./Bolt_nut_v2/data/val"
destination_folder = "./Bolt_nut_v2/labels/val"

# Ensure the destination folder exists
os.makedirs(destination_folder, exist_ok=True)

# Loop through files in the source folder
for file_name in os.listdir(source_folder):
    if file_name.endswith(".txt"):  # Check if it's a .txt file
        source_path = os.path.join(source_folder, file_name)
        destination_path = os.path.join(destination_folder, file_name)
        
        # Move the file
        shutil.move(source_path, destination_path)
        print(f"Moved: {file_name} -> {destination_folder}")

print("All .txt files have been moved successfully!")
