import os
import tkinter as tk
from tkinter import filedialog, ttk
import threading
import subprocess
from tkinter import messagebox
import configparser
import time
import re

# Initialize GUI window
window = tk.Tk()
window.title("Arlen's Hashcat Tool")
window.geometry("600x600")

# Config file setup
config = configparser.ConfigParser()
config_file = 'config.ini'

# Load existing configuration if available
def load_config():
    global hashcatPath, hcxpcapngtoolPath, clear_command
    if os.path.exists(config_file):
        config.read(config_file)
        hashcatPath = config.get('Paths', 'hashcatPath', fallback='')
        hcxpcapngtoolPath = config.get('Paths', 'hcxpcapngtoolPath', fallback='')
        clear_command = config.get('Settings', 'clear_command', fallback='cls')
    else:
        hashcatPath = ''
        hcxpcapngtoolPath = ''
        clear_command = 'cls'

# Save current configuration
def save_config():
    config['Paths'] = {
        'hashcatPath': hashcatPath,
        'hcxpcapngtoolPath': hcxpcapngtoolPath
    }
    config['Settings'] = {
        'clear_command': clear_command
    }
    with open(config_file, 'w') as configfile:
        config.write(configfile)

# Load the configuration at startup
load_config()

# Paths
pcapPath = os.path.expanduser(r'C:\caps')
hccapPath = os.path.expanduser(r'C:\caps\hccap')
dictPath = r'C:\Dictionaries'

# Global variables
pcap = 'x'
hccap = 'x'
dictionaries = []
progress = 0
status_var = tk.StringVar(value="Idle")

# Helper to clear terminal
def chunk():
    os.system(clear_command)

# Crack function allowing multiple dictionaries
def crack_multiple_dicts(hccap, dictionaries):
    status_var.set("Running")
    window.update_idletasks()
    
    for idx, dictionary in enumerate(dictionaries):
        # Run the hashcat command and capture the output in real time
        mycommand = f'{hashcatPath} -m 22000 -a 0 "{hccap}" "{dictionary}" -w 3 --status --status-timer=5'
        process = subprocess.Popen(mycommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')

        # Monitor progress by reading the process output in real time
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())  # Print to terminal for debugging purposes
                # Extract progress percentage using regex
                match = re.search(r'Progress.*?([0-9]+\.[0-9]+)%', output)
                if match:
                    try:
                        progress_value = float(match.group(1))
                        progress_var.set(int(progress_value))
                        window.update_idletasks()
                    except ValueError:
                        pass

        # If hashcat returns a success code, stop cracking
        if process.returncode == 0:
            status_var.set("Found")
            status_label.config(fg="green")
            break
    else:
        status_var.set("Exhausted")
        status_label.config(fg="red")

    # Set progress to 100% when done
    progress_var.set(100)
    window.update_idletasks()

# Brute force function
def brute_force(hccap, length):
    status_var.set("Running")
    window.update_idletasks()

    # Create mask based on length
    mask = "?a" * length

    # Run the hashcat brute force command
    mycommand = f'{hashcatPath} -m 22000 "{hccap}" -a 3 "{mask}" -w 3 --status --status-timer=5'
    process = subprocess.Popen(mycommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')

    # Monitor progress by reading the process output in real time
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())  # Print to terminal for debugging purposes
            # Extract progress percentage using regex
            match = re.search(r'Progress.*?([0-9]+\.[0-9]+)%', output)
            if match:
                try:
                    progress_value = float(match.group(1))
                    progress_var.set(int(progress_value))
                    window.update_idletasks()
                except ValueError:
                    pass

    # If hashcat returns a success code
    if process.returncode == 0:
        status_var.set("Found")
        status_label.config(fg="green")
    else:
        status_var.set("Exhausted")
        status_label.config(fg="red")

    # Set progress to 100% when done
    progress_var.set(100)
    window.update_idletasks()

# GUI elements
def browse1():
    global pcap
    window.filename = filedialog.askopenfilename(initialdir=pcapPath, title="Select file",
                                                 filetypes=(("cap files", "*.cap"), ("all files", "*.*")))
    pcap = window.filename
    print('File:', pcap, 'loaded')

def browse2():
    global hccap
    window.filename = filedialog.asksaveasfilename(initialdir=hccapPath, title="Save as",
                                                   filetypes=(("22000 files", "*.22000"), ("hccap files", "*.hccap"), ("all files", "*.*")))
    hccap = window.filename
    print('File:', hccap, 'loaded')

def browse3():
    global hccap
    window.filename = filedialog.askopenfilename(initialdir=hccapPath, title="Select Hccap File",
                                                 filetypes=(("22000 files", "*.22000"), ("hccap files", "*.hccap"), ("all files", "*.*")))
    hccap = window.filename
    print('File:', hccap, 'loaded')

def browse4():
    global dictionaries
    window.filenames = filedialog.askopenfilenames(initialdir=dictPath, title="Select dictionary files",
                                                   filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
    dictionaries = list(window.filenames)
    print('Dictionaries:', dictionaries, 'loaded')

def browse_hashcat():
    global hashcatPath
    window.filename = filedialog.askopenfilename(title="Select Hashcat executable",
                                                 filetypes=(("Executable files", "*.exe;*.bin"), ("all files", "*.*")))
    hashcatPath = window.filename
    print('Hashcat Path:', hashcatPath, 'loaded')
    save_config()

def browse_hcxpcapngtool():
    global hcxpcapngtoolPath
    window.filename = filedialog.askopenfilename(title="Select hcxpcapngtool executable",
                                                 filetypes=(("Executable files", "*.exe;*.bin"), ("all files", "*.*")))
    hcxpcapngtoolPath = window.filename
    print('hcxpcapngtool Path:', hcxpcapngtoolPath, 'loaded')
    save_config()

def convert2hccap():
    if not hcxpcapngtoolPath:
        messagebox.showerror("Error", "Please specify the path to hcxpcapngtool first.")
    else:
        mycommand = f'{hcxpcapngtoolPath} "{pcap}" -o "{hccap}"'
        os.system(mycommand)

def hashcat():
    if hccap == 'x' or not dictionaries:
        print("You need to load an hccap file and at least one dictionary file first")
    elif not hashcatPath:
        messagebox.showerror("Error", "Please specify the path to Hashcat first.")
    else:
        # Run the cracking process in a separate thread to avoid freezing the GUI
        threading.Thread(target=crack_multiple_dicts, args=(hccap, dictionaries)).start()

def hashcatShow():
    if hccap == 'x':
        print("You need to load a cracked hccap first")
    elif not hashcatPath:
        messagebox.showerror("Error", "Please specify the path to Hashcat first.")
    else:
        mycommand = f'{hashcatPath} -m 22000 "{hccap}" --show'
        os.system(mycommand)

def bruteForce():
    if hccap == 'x':
        print("You need to load an hccap file first")
    elif not hashcatPath:
        messagebox.showerror("Error", "Please specify the path to Hashcat first.")
    else:
        try:
            length = int(length_entry.get())
            if length < 1:
                raise ValueError
            # Run the brute force process in a separate thread to avoid freezing the GUI
            threading.Thread(target=brute_force, args=(hccap, length)).start()
        except ValueError:
            messagebox.showerror("Error", "Please specify a valid length (positive integer) for brute forcing.")

def settings():
    settings_window = tk.Toplevel(window)
    settings_window.title("Settings")
    settings_window.geometry("400x200")

    tk.Button(settings_window, text="Hashcat Path", command=browse_hashcat, width=20).grid(column=0, row=0, sticky="W", pady=5)
    tk.Button(settings_window, text="hcxpcapngtool Path", command=browse_hcxpcapngtool, width=20).grid(column=0, row=1, sticky="W", pady=5)

    def set_os_type():
        global clear_command
        if os_type.get() == "Linux":
            clear_command = 'clear'
        else:
            clear_command = 'cls'
        save_config()

    os_type = tk.StringVar(value="Windows" if clear_command == 'cls' else "Linux")
    tk.Label(settings_window, text="Operating System: ").grid(column=0, row=2, sticky="W", pady=5)
    tk.Radiobutton(settings_window, text="Windows", variable=os_type, value="Windows", command=set_os_type).grid(column=1, row=2, sticky="W")
    tk.Radiobutton(settings_window, text="Linux", variable=os_type, value="Linux", command=set_os_type).grid(column=2, row=2, sticky="W")

# GUI Layout
pad_x, pad_y = 10, 5

# Convert to hccap section
tk.Label(text="Convert a cap to .22000").grid(column=0, row=0, columnspan=4, sticky="W", padx=pad_x, pady=pad_y)
tk.Button(text="Source", command=browse1, width=15).grid(column=0, row=1, sticky="W", padx=pad_x, pady=pad_y)
tk.Button(text="Destination", command=browse2, width=15).grid(column=1, row=1, sticky="W", padx=pad_x, pady=pad_y)
tk.Button(text="Convert to .22000", command=convert2hccap, width=35).grid(column=2, row=1, columnspan=2, sticky="W", padx=pad_x, pady=pad_y)

# Crack hash section
tk.Label(text="Crack Hash").grid(column=0, row=2, columnspan=4, sticky="W", padx=pad_x, pady=pad_y)
tk.Label(text="Hccap File").grid(column=0, row=3, sticky="W", padx=pad_x, pady=pad_y)
tk.Button(text="Select Hccap File", command=browse3, width=20).grid(column=1, row=3, sticky="W", padx=pad_x, pady=pad_y)
tk.Label(text="Dictionary Files").grid(column=2, row=3, sticky="W", padx=pad_x, pady=pad_y)
tk.Button(text="Select Dictionaries", command=browse4, width=20).grid(column=3, row=3, sticky="W", padx=pad_x, pady=pad_y)
tk.Button(text="Crack Hash", command=hashcat, width=50).grid(column=0, row=4, columnspan=4, sticky="W", padx=pad_x, pady=pad_y)
tk.Button(text="Show Known", command=hashcatShow, width=50).grid(column=0, row=5, columnspan=4, sticky="W", padx=pad_x, pady=pad_y)

# Brute force section
tk.Label(text="Brute Force Options").grid(column=0, row=6, columnspan=4, sticky="W", padx=pad_x, pady=pad_y)
tk.Label(text="Length").grid(column=0, row=7, sticky="W", padx=pad_x, pady=pad_y)
length_entry = tk.Entry(window, width=10)
length_entry.grid(column=1, row=7, sticky="W", padx=pad_x, pady=pad_y)
tk.Button(text="Start Brute Force", command=bruteForce, width=20).grid(column=3, row=7, sticky="W", padx=pad_x, pady=pad_y)

# Progress bar
tk.Label(text="Progress:").grid(column=0, row=8, sticky="W", padx=pad_x, pady=pad_y)
progress_var = tk.IntVar()
progress_bar = ttk.Progressbar(window, variable=progress_var, maximum=100)
progress_bar.grid(column=1, row=8, columnspan=3, sticky="W", padx=pad_x, pady=pad_y)

# Status label
tk.Label(text="Status:").grid(column=0, row=9, sticky="W", padx=pad_x, pady=pad_y)
status_label = tk.Label(window, textvariable=status_var, fg="black")
status_label.grid(column=1, row=9, columnspan=3, sticky="W", padx=pad_x, pady=pad_y)

# Settings button
tk.Button(window, text="Settings", command=settings, width=15).grid(column=3, row=0, sticky="E", padx=pad_x, pady=pad_y)

window.mainloop()
