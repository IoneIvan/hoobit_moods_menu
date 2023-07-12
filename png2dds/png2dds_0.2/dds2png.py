import os
from PIL import Image

def convert_dds_to_png(dds_folder):
    # Create a new folder for the converted images
    png_folder = os.path.join(dds_folder, "converted_images")
    os.makedirs(png_folder, exist_ok=True)

    # Convert each .dds image to .png and save in the new folder
    for filename in os.listdir(dds_folder):
        if filename.endswith(".dds"):
            dds_path = os.path.join(dds_folder, filename)
            png_path = os.path.join(png_folder, os.path.splitext(filename)[0] + ".png")

            try:
                # Open the .dds image and convert it to .png
                with Image.open(dds_path) as img:
                    img.save(png_path, "PNG")
                print(f"Converted {filename} successfully.")
            except Exception as e:
                print(f"Failed to convert {filename}. Error: {str(e)}")

    print("Conversion completed.")

# Ask the user for the folder path containing .dds images
dds_folder = input("Enter the path to the folder containing .dds images: ")

# Convert the .dds images to .png and save in a new folder
convert_dds_to_png(dds_folder)
