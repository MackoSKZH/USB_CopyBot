import os
import shutil
import psutil
import tkinter as tk
from tkinter import messagebox
import time
import zipfile
import sys

def get_mounted_devices():
    """Returns a list of mounted disk devices with their mount points."""
    devices = {}
    for partition in psutil.disk_partitions():
        if 'cdrom' in partition.opts or partition.fstype == '':
            continue
        devices[partition.device] = partition.mountpoint
    return devices

def zip_documents(source_path, zip_path):
    """Creates a ZIP archive of all files from the source."""
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, dirs, files in os.walk(source_path):
            for file in files:
                zipf.write(os.path.join(root, file), 
                           os.path.relpath(os.path.join(root, file), 
                                           os.path.join(source_path, '..')))

def handle_new_usb(device_path):
    """Handles the tasks to be performed when a new USB is detected."""
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    new_folder_path = os.path.join(desktop_path, 'USB_Documents')
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)

    zip_file_path = os.path.join(new_folder_path, 'USB_Documents.zip')
    zip_documents(device_path, zip_file_path)

    sys.exit(0)
    #show_message(device_path)

def show_message(device_path):
    """Displays a message in a dialog box with the device path."""
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("USB Detection", f"ZIP file created from USB at: {device_path}")
    root.destroy()

original_devices = get_mounted_devices()

while True:
    current_devices = get_mounted_devices()
    new_devices = set(current_devices.keys()) - set(original_devices.keys())
    
    if new_devices:
        for device in new_devices:
            handle_new_usb(current_devices[device])
        original_devices = current_devices

    time.sleep(5)