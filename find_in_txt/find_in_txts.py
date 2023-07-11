import glob
import tkinter as tk
from tkinter import filedialog, messagebox

def search_files():
    folder_path = folder_entry.get()
    search_string = search_entry.get()

    file_list = glob.glob(folder_path + "/*.txt")
    matching_files = []

    for file_path in file_list:
        with open(file_path, 'r') as file:
            content = file.read()
            if search_string in content:
                matching_files.append(file_path)

    if matching_files:
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Matching files found:\n")
        for file_path in matching_files:
            result_text.insert(tk.END, file_path + "\n")
    else:
        messagebox.showinfo("No Matching Files", "No matching files found.")

def browse_folder():
    folder_path = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(tk.END, folder_path)

# Create the GUI
window = tk.Tk()
window.title("File Search")
window.geometry("800x300")

# Folder path label and entry
folder_label = tk.Label(window, text="Folder Path:")
folder_label.pack()
folder_entry = tk.Entry(window, width = 50)
folder_entry.pack()
browse_button = tk.Button(window, text="Browse", command=browse_folder)
browse_button.pack()

# Search string label and entry
search_label = tk.Label(window, text="Search String:")
search_label.pack()
search_entry = tk.Entry(window)
search_entry.pack()

# Search button
search_button = tk.Button(window, text="Search", command=search_files)
search_button.pack()

# Result text box
result_text = tk.Text(window)
result_text.pack()

# Start the GUI main loop
window.mainloop()
