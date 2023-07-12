import os
import subprocess

# Prompt user for the path to the folder
folder_path = input("Enter the path to the folder containing the images: ")

# Create the output folder if it doesn't exist
output_folder = os.path.join(folder_path, "output")
os.makedirs(output_folder, exist_ok=True)

# Get a list of all image files in the folder
image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

# Loop through each image file and run the command
for image_file in image_files:
    input_path = os.path.join(folder_path, image_file)
    output_path = os.path.join(output_folder, image_file)
    
    # Run the command using subprocess
    command = f'texconv.exe -f BC2_UNORM -o "{output_folder}" "{input_path}"'
    subprocess.run(command, shell=True)

print("Conversion completed!")
