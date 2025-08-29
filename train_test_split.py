import os
import random
import shutil

def split_dataset(img_folder, label_folder, train_ratio=0.8, val_ratio=0.1, test_ratio=0.1):
    # Get a list of image files
    img_files = [f for f in os.listdir(img_folder) if f.endswith('.JPG')]
    total_samples = len(img_files)

    # Calculate the number of samples for each set
    train_samples = int(total_samples * train_ratio)
    val_samples = int(total_samples * val_ratio)
    test_samples = total_samples - train_samples - val_samples

    # Randomly shuffle the list of image files
    random.shuffle(img_files)

    # Split the dataset
    train_set = img_files[:train_samples]
    val_set = img_files[train_samples:train_samples + val_samples]
    test_set = img_files[train_samples + val_samples:]

    # Create folders for train, val, and test sets
    train_folder = os.path.join(img_folder, 'train')
    val_folder = os.path.join(img_folder, 'val')
    test_folder = os.path.join(img_folder, 'test')

    os.makedirs(train_folder, exist_ok=True)
    os.makedirs(val_folder, exist_ok=True)
    os.makedirs(test_folder, exist_ok=True)

    # Move image files to respective folders
    for file_name in train_set:
        img_path = os.path.join(img_folder, file_name)
        label_path = os.path.join(label_folder, file_name.replace('.JPG', '.txt'))
        shutil.move(img_path, os.path.join(train_folder, file_name))
        shutil.move(label_path, os.path.join(train_folder, file_name.replace('.JPG', '.txt')))

    for file_name in val_set:
        img_path = os.path.join(img_folder, file_name)
        label_path = os.path.join(label_folder, file_name.replace('.JPG', '.txt'))
        shutil.move(img_path, os.path.join(val_folder, file_name))
        shutil.move(label_path, os.path.join(val_folder, file_name.replace('.JPG', '.txt')))

    for file_name in test_set:
        img_path = os.path.join(img_folder, file_name)
        label_path = os.path.join(label_folder, file_name.replace('.JPG', '.txt'))
        shutil.move(img_path, os.path.join(test_folder, file_name))
        shutil.move(label_path, os.path.join(test_folder, file_name.replace('.JPG', '.txt')))

# Set your paths
img_folder = './data'
label_folder = './labels'

# Call the function to split the dataset
split_dataset(img_folder, label_folder)
