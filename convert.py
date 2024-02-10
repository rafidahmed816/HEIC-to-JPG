from PIL import Image
import pillow_heif
import os
import tkinter as tk
from tkinter import filedialog
import threading

pillow_heif.register_heif_opener()

class ConversionThread(threading.Thread):
    def __init__(self, heic_directory, jpg_directory):
        threading.Thread.__init__(self)
        self.heic_directory = heic_directory
        self.jpg_directory = jpg_directory
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        # Create the output directory if it doesn't exist
        if not os.path.exists(self.jpg_directory):
            os.makedirs(self.jpg_directory)

        # Iterate through HEIC files in the directory
        for filename in os.listdir(self.heic_directory):
            if self.stopped():
                break
            if filename.lower().endswith('.heic'):
                heic_path = os.path.join(self.heic_directory, filename)
                
                # Open the HEIC file
                img = Image.open(heic_path)
                
                # Save as JPG in the specified directory
                jpg_path = os.path.join(self.jpg_directory, os.path.splitext(filename)[0] + '.jpg')
                img.save(jpg_path, format='JPEG')
        
        print("Conversion complete.")

def browse_input_folder():
    folder_path = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder_path)

def browse_output_folder():
    folder_path = filedialog.askdirectory()
    jpg_entry.delete(0, tk.END)
    jpg_entry.insert(0, folder_path)

def convert():
    global conversion_thread
    heic_directory = folder_entry.get()
    jpg_directory = jpg_entry.get()
    conversion_thread = ConversionThread(heic_directory, jpg_directory)
    conversion_thread.start()

def stop():
    if conversion_thread and conversion_thread.is_alive():
        conversion_thread.stop()
        conversion_thread.join()
        print("Conversion stopped.")

# Create a tkinter window
root = tk.Tk()
root.title("HEIC to JPG Converter")

# Folder selection
folder_label = tk.Label(root, text="Select Folder Containing HEIC Files:")
folder_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

folder_entry = tk.Entry(root, width=50)
folder_entry.grid(row=0, column=1, padx=5, pady=5)

folder_button = tk.Button(root, text="Browse", command=browse_input_folder)
folder_button.grid(row=0, column=2, padx=5, pady=5)

# Output directory selection
jpg_label = tk.Label(root, text="Select Output JPG Folder:")
jpg_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

jpg_entry = tk.Entry(root, width=50)
jpg_entry.grid(row=1, column=1, padx=5, pady=5)

jpg_button = tk.Button(root, text="Browse", command=browse_output_folder)
jpg_button.grid(row=1, column=2, padx=5, pady=5)

# Convert and Stop buttons
convert_button = tk.Button(root, text="Convert", command=convert)
convert_button.grid(row=2, column=1, padx=5, pady=5)

stop_button = tk.Button(root, text="Stop", command=stop, bg="red")
stop_button.grid(row=2, column=2, padx=5, pady=5)

conversion_thread = None

root.mainloop()
