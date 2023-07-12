import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar

def convert_images():
    # Get the selected or manually entered folder path
    folder_path = folder_entry.get()

    # Validate if the path exists
    if not os.path.exists(folder_path):
        messagebox.showerror("Invalid Path", "The specified folder path does not exist.")
        return

    # Create the output folder path
    output_folder = os.path.join(script_path, "output")

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Get a list of all image files in the folder
    image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    # Calculate the total number of files
    total_files = len(image_files)

    # Configure the progress bar
    progress_bar.configure(maximum=total_files, value=0)
    progress_label.configure(text="Converting images...")

    # Loop through each image file and run the command
    for index, image_file in enumerate(image_files, start=1):
        input_path = os.path.join(folder_path, image_file)
        output_path = os.path.join(output_folder, image_file)

        # Run the command using subprocess
        command = f'texconv.exe -f BC2_UNORM -o "{output_folder}" "{input_path}"'
        subprocess.run(command, shell=True)

        # Update the progress bar value
        progress_bar.configure(value=index)
        window.update()

    progress_label.configure(text="Conversion complete!")
    messagebox.showinfo("Conversion Complete", "Image conversion completed!")

def select_folder():
    # Prompt user to select the folder containing the images
    folder_path = filedialog.askdirectory(title="Select the folder containing the images")
    if folder_path:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(tk.END, folder_path)

# Get the current script's file path
script_path = os.path.dirname(os.path.abspath(__file__))

# Create the main window
window = tk.Tk()
window.title("Image Converter")
window.geometry("400x250")

# Create a label, entry field, and button for selecting the folder
label = tk.Label(window, text="Select the folder containing the images")
label.pack(pady=10)

folder_entry = tk.Entry(window, width=50)
folder_entry.pack()

select_button = tk.Button(window, text="Browse", command=select_folder)
select_button.pack()

# Create a button to start the conversion
convert_button = tk.Button(window, text="Start Conversion", command=convert_images)
convert_button.pack(pady=10)

# Create a progress bar
progress_bar = Progressbar(window, orient=tk.HORIZONTAL, length=200, mode='determinate')
progress_bar.pack(pady=10)

# Create a label for progress status
progress_label = tk.Label(window, text="")
progress_label.pack()

# Run the main window's event loop
window.mainloop()
