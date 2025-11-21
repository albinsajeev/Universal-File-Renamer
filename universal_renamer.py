import os
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
import threading
import re
import uuid

# --- THE CORE LOGIC ---
def process_universal_rename(user_selected_path, log_func, progress_func, status_func):
    # 1. Normalize Path
    raw_path = os.path.normpath(user_selected_path)
    long_path_prefix = "\\\\?\\"

    if os.name == 'nt' and not raw_path.startswith(long_path_prefix):
        folder_path = long_path_prefix + raw_path
    else:
        folder_path = raw_path

    log_func(f"--- TARGET: {raw_path} ---\n")
    status_func("Status: Scanning files...")

    try:
        # 2. Get Files
        try:
            files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        except OSError as e:
            status_func("Status: Error Accessing Folder")
            messagebox.showerror("Error", f"Could not access path:\n{e}")
            return

        # Ignore the script itself and system files
        ignore_files = ['universal_renamer.exe', 'universal_renamer.py', 'desktop.ini', 'thumbs.db']
        files = [f for f in files if f.lower() not in ignore_files]

        if not files:
            progress_func(100)
            status_func("Status: No files found")
            log_func("Folder is empty or contains no valid files.\n")
            return

        # 3. SORT FIRST (FIXED LOGIC)
        # We return a tuple: (Number, Name). 
        # Python can compare (int, str) vs (float, str) safely.
        def smart_sort_key(name):
            numbers = re.findall(r'\d+', name)
            if numbers:
                # Found a number: Sort by that number first
                return (int(numbers[0]), name)
            else:
                # No number: Assign 'Infinity' so it goes to the end of the list
                return (float('inf'), name)
        
        files.sort(key=smart_sort_key)
        total_files = len(files)

        log_func(f"Found {total_files} files. Starting Rename...\n")
        
        # --- STEP 1: RENAME TO TEMP NAMES (0-50%) ---
        status_func("Status: Phase 1/2 - Safe Temp Rename...")
        temp_map = [] 

        for index, filename in enumerate(files):
            percentage = int(((index + 1) / total_files) * 50)
            progress_func(percentage)

            old_path = os.path.join(folder_path, filename)
            ext = os.path.splitext(filename)[1]
            
            temp_name = f"__temp_{uuid.uuid4().hex}{ext}"
            temp_path = os.path.join(folder_path, temp_name)
            
            try:
                os.rename(old_path, temp_path)
                temp_map.append(temp_name)
            except OSError as e:
                log_func(f"Error in Phase 1 for {filename}: {e}\n")
                continue

        # --- STEP 2: RENAME TO 1, 2, 3... (50-100%) ---
        status_func("Status: Phase 2/2 - Numbering (1, 2, 3...)...")
        count = 1
        
        for index, temp_filename in enumerate(temp_map):
            percentage = 50 + int(((index + 1) / len(temp_map)) * 50)
            progress_func(percentage)

            temp_path = os.path.join(folder_path, temp_filename)
            ext = os.path.splitext(temp_filename)[1]
            
            new_name = f"{count}{ext}"
            new_path = os.path.join(folder_path, new_name)
            
            try:
                os.rename(temp_path, new_path)
                log_func(f"Renamed: {new_name}\n")
                count += 1
            except OSError as e:
                log_func(f"Error in Phase 2: {e}\n")

        progress_func(100)
        status_func("Status: Completed")
        log_func("--- ALL DONE ---\n")
        messagebox.showinfo("Success", "All files renamed to 1, 2, 3...!")

    except Exception as e:
        status_func("Status: Critical Error")
        log_func(f"CRITICAL ERROR: {e}\n")
        messagebox.showerror("Critical Error", f"An unexpected error occurred:\n{e}")

# --- GUI SETUP ---
def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        btn_select.config(state=tk.DISABLED, text="Running...")
        progress_bar['value'] = 0
        lbl_status.config(text="Status: Starting...", fg="blue")
        text_log.delete(1.0, tk.END)
        thread = threading.Thread(target=run_thread, args=(folder_selected,))
        thread.start()

def run_thread(folder):
    process_universal_rename(folder, update_log, update_progress, update_status)
    btn_select.config(state=tk.NORMAL, text="Select Folder")

def update_log(message):
    text_log.insert(tk.END, message)
    text_log.see(tk.END)

def update_progress(val):
    progress_bar['value'] = val
    root.update_idletasks()

def update_status(msg):
    lbl_status.config(text=msg)
    if "Error" in msg:
        lbl_status.config(fg="red")
    elif "Completed" in msg:
        lbl_status.config(fg="green")
    else:
        lbl_status.config(fg="blue")

# --- GUI LAYOUT ---
root = tk.Tk()
root.title("Universal File Renamer")
root.geometry("600x500")

tk.Label(root, text="Universal File Renamer", font=("Arial", 16, "bold")).pack(pady=(15, 5))
tk.Label(root, text="Renames ALL files to 1.ext, 2.ext, 3.ext (Keeps original format)", font=("Arial", 10)).pack(pady=5)
tk.Label(root, text="Warning: Original names will be lost.", font=("Arial", 8), fg="red").pack(pady=0)

btn_select = tk.Button(root, text="Select Folder to Rename", command=select_folder, height=2, width=25, bg="#673AB7", fg="white", font=("Arial", 11, "bold"))
btn_select.pack(pady=15)

lbl_status = tk.Label(root, text="Status: Waiting for input...", font=("Arial", 11, "bold"), fg="gray")
lbl_status.pack(pady=5)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=500, mode="determinate")
progress_bar.pack(pady=10)

text_log = scrolledtext.ScrolledText(root, height=12, width=70, font=("Consolas", 9))
text_log.pack(padx=10, pady=10)

root.mainloop()