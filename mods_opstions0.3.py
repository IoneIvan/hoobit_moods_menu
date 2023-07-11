import os
import json
import shutil
import subprocess
import tkinter as tk

def create_mods_folder():
    if not os.path.exists("mods"):
        os.makedirs("mods")

def get_mod_list():
    mod_list = []
    for folder_name in os.listdir("mods"):
        if os.path.isdir(os.path.join("mods", folder_name)):
            mod_list.append(folder_name)
    return mod_list

def add_mod(mod_path):
    if not os.path.isfile(mod_path) or not mod_path.endswith(".hb"):
        print("Invalid mod file.")
        return
    
    mod_name = os.path.splitext(os.path.basename(mod_path))[0]
    mod_folder = os.path.join("mods", mod_name)
    
    if os.path.exists(mod_folder):
        print("Mod already added.")
        return
    
    shutil.copytree(os.path.dirname(mod_path), mod_folder)
    
    mod_list = get_mod_list()
    mod_list.append(mod_name)
    save_mod_list(mod_list)

def save_mod_list(mod_list):
    with open("mods/mod_list.json", "w") as file:
        json.dump(mod_list, file)

def load_mod_list():
    with open("mods/mod_list.json", "r") as file:
        mod_list = json.load(file)
    return mod_list

def activate_mod(mod_name):
    mod_list = load_mod_list()
    mod_folder = os.path.join("mods", mod_name)
    if not os.path.exists(mod_folder):
        print("Mod not found in the mods folder.")
        return
    if mod_name in mod_list:
        print("Mod is already activated.")
        return
    mod_list.append(mod_name)
    save_mod_list(mod_list)
    print("Mod is now activated")

def deactivate_mod(mod_name):
    mod_list = load_mod_list()
    mod_folder = os.path.join("mods", mod_name)
    if not os.path.exists(mod_folder):
        print("Mod not found in the mods folder.")
        return
    if mod_name not in mod_list:
        print("Mod is not activated.")
        return
    mod_list.remove(mod_name)
    print("Mod is now deactivated")
    save_mod_list(mod_list)


def play_game():
    mod_list = load_mod_list()
    
    for mod_name in mod_list:
        with open(os.path.join("mods", mod_name, f"{mod_name}.hb"), "r") as file:
            mod_data = json.load(file)
        
        executable_file = mod_data["executableFile"]
        additional_files = mod_data["additionalFiles"]
        wait_for_game_open = mod_data.get("waitForGameOpen", False)
        
        print(f"Launching the game with {mod_name}...")
        
        # Launch the executable file
        game_process = subprocess.Popen(os.path.join("mods", mod_name, executable_file))
        
        if wait_for_game_open:
            # Wait for the game process to open
            game_process.wait()
        
        for additional_file in additional_files:
            file_name = additional_file["fileName"]
            levels = additional_file["levels"]
            
            print(f" - {mod_name} - Additional File: {file_name}, Levels: {levels}")
            # Perform any necessary actions for each additional file, e.g., copying files to the game
        
        # Wait for the game process to close
        game_process.wait()
        
        print(f"Mod {mod_name} finished.")
    
    # All mods have been processed, close the program
    print("All mods have been successfully added. Closing the program.")

def main():
    create_mods_folder()
    mod_list = get_mod_list()
    print("Available mods:")
    for mod_name in mod_list:
        print(mod_name)
    
    root = tk.Tk()
    root.title("Mod Manager")
    
    checkbox_vars = {}
    for mod_name in mod_list:
        checkbox_vars[mod_name] = tk.BooleanVar()
        checkbox_vars[mod_name].set(False)
    
    def add_mod_callback():
        mod_path = entry.get()
        add_mod(mod_path)
        entry.delete(0, tk.END)
        refresh_mod_list()
    
    def activate_mod_callback():
        for mod_name, var in checkbox_vars.items():
            if var.get():
                activate_mod(mod_name)
            else:
                deactivate_mod(mod_name)
    
    def deactivate_mod_callback():
        for mod_name, var in checkbox_vars.items():
            if var.get():
                deactivate_mod(mod_name)
    
    def play_game_callback():
        activate_mod_callback()
        play_game()
        root.destroy()
    
    def refresh_mod_list():
        mod_list = get_mod_list()
        checkbox_vars.clear()
        for widget in mod_frame.winfo_children():
            widget.destroy()
        
        for mod_name in mod_list:
            checkbox_vars[mod_name] = tk.BooleanVar()
            checkbox_vars[mod_name].set(mod_name in load_mod_list())
            tk.Checkbutton(mod_frame, text=mod_name, variable=checkbox_vars[mod_name]).pack(anchor="w")
    
    entry_frame = tk.Frame(root)
    entry_frame.pack(padx=10, pady=10)
    entry_label = tk.Label(entry_frame, text="Enter the path to the mod file: ")
    entry_label.pack(side="left")
    entry = tk.Entry(entry_frame, width=50)
    entry.pack(side="left")
    add_mod_button = tk.Button(entry_frame, text="Add Mod", command=add_mod_callback)
    add_mod_button.pack(side="left")
    
    mod_frame = tk.Frame(root)
    mod_frame.pack(padx=10, pady=10)
    refresh_mod_list()
    
    activate_mod_button = tk.Button(root, text="Activate Mod(s)", command=activate_mod_callback)
    activate_mod_button.pack(pady=5)
    

    
    play_game_button = tk.Button(root, text="Play Game", command=play_game_callback)
    play_game_button.pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    main()
