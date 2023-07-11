import json
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog


def add_additional_file():
    file_name = file_entry.get()
    if file_name:
        levels = levels_entry.get().split(',')
        additional_file = {
            "fileName": file_name.strip(),
            "levels": [level.strip() for level in levels]
        }
        mod_data["additionalFiles"].append(additional_file)
        file_entry.delete(0, tk.END)
        levels_entry.delete(0, tk.END)
        update_json_preview()


def process_folder_files():
    folder_path = filedialog.askdirectory()
    if folder_path:
        levels = levels_entry.get().split(',')
        if os.path.isdir(folder_path):
            for file_name in os.listdir(folder_path):
                additional_file = {
                    "fileName": file_name,
                    "levels": [level.strip() for level in levels]
                }
                mod_data["additionalFiles"].append(additional_file)
            file_entry.delete(0, tk.END)
            levels_entry.delete(0, tk.END)
            update_json_preview()
        else:
            messagebox.showerror("Invalid Folder Path", "Invalid folder path.")


def update_json_preview():
    if json_text is not None:
        # Get current scroll position
        scroll_pos = json_text.yview()

        json_text.delete('1.0', tk.END)
        json_text.insert(tk.END, json.dumps(mod_data, indent=2))

        # Restore scroll position
        json_text.yview_moveto(scroll_pos[0])


def show_json_preview():
    if json_preview_window is not None and json_preview_window.winfo_exists():
        update_json_preview()
        json_preview_window.lift()
    else:
        create_json_preview_window()


def create_json_preview_window():
    global json_preview_window, json_text

    json_preview_window = tk.Toplevel(root)
    json_preview_window.title("JSON Preview")
    json_preview_window.geometry("600x400")

    json_text = tk.Text(json_preview_window)
    json_text.pack()
    update_json_preview()


def save_config():
    mod_data["name"] = name_entry.get()
    mod_data["executableFile"] = executable_entry.get()
    mod_data["waitForGameOpen"] = bool(wait_var.get())
    update_json_preview()

    mod_name = mod_data["name"]
    file_name = f"{mod_name}.hb"
    file_path = os.path.join(os.getcwd(), file_name)

    with open(file_path, "w") as file:
        json.dump(mod_data, file, indent=2)

    messagebox.showinfo("Configuration Saved", f"JSON configuration saved as '{file_name}' in the same folder.")
    root.destroy()



def exit_program():
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        root.destroy()


root = tk.Tk()
root.title("Mod Configuration")
root.geometry("600x400")

mod_data = {
    "name": "",
    "executableFile": "",
    "additionalFiles": [],
    "waitForGameOpen": False
}

name_label = tk.Label(root, text="Mod Name:")
name_label.pack()
name_entry = tk.Entry(root)
name_entry.pack()

executable_label = tk.Label(root, text="Executable File:")
executable_label.pack()
executable_entry = tk.Entry(root)
executable_entry.pack()

wait_var = tk.IntVar()
wait_checkbox = tk.Checkbutton(root, text="Wait for Game to Open", variable=wait_var)
wait_checkbox.pack()

file_label = tk.Label(root, text="Additional File:")
file_label.pack()
file_entry = tk.Entry(root)
file_entry.pack()

levels_label = tk.Label(root, text="Levels (comma-separated):")
levels_label.pack()
levels_entry = tk.Entry(root)
levels_entry.pack()

add_button = tk.Button(root, text="Add Additional File", command=add_additional_file)
add_button.pack()

folder_button = tk.Button(root, text="Process Files in Folder", command=process_folder_files)
folder_button.pack()

json_preview_button = tk.Button(root, text="Show JSON Preview", command=show_json_preview)
json_preview_button.pack()

json_preview_window = None
json_text = None

save_button = tk.Button(root, text="Save Configuration", command=save_config)
save_button.pack()

exit_button = tk.Button(root, text="Exit", command=exit_program)
exit_button.pack()

root.mainloop()
