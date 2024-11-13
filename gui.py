import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import messagebox
import main
import os
import threading
import sys


class ConsoleRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        # Insert console message into the text widget
        self.text_widget.insert(tk.END, message)
        # Auto-scroll to the bottom
        self.text_widget.see(tk.END)

    def flush(self):
        pass  # Required for compatibility with Python's stdout


def process_audio(file_path):
    valid_extensions = {
        ".wav",
        ".mp3",
        ".flac",
        ".ogg",
        ".m4a",
        ".opus",
        ".mp4",
        ".mkv",
    }
    # Correct file path if it has extra characters from drag-and-drop
    file_path = file_path.strip("{}")
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension not in valid_extensions:
        messagebox.showerror(
            "Invalid File", "Please drop a valid audio file (e.g., .wav, .mp3, .flac)"
        )
        return

    output_file = os.path.join(os.path.dirname(file_path), "output.mp3")

    # Lock drag-and-drop and disable the window while processing
    label.config(text="Processing... Please wait.")
    root.drop_target_unregister()  # Correct way to unregister the drop target
    root.config(cursor="wait")

    # Run the audio processing in a separate thread
    thread = threading.Thread(
        target=run_audio_processing, args=(file_path, output_file)
    )
    thread.start()


def run_audio_processing(file_path, output_file):
    print(f"Starting processing of {file_path}...")
    main.main(file_path, output_file)
    print("Processing complete.")
    messagebox.showinfo(
        "Processing Complete", f"Processed file saved as: {output_file}"
    )
    clear_console()

    # Close the window after processing is done
    root.quit()


def on_drop(event):
    file_path = event.data
    process_audio(file_path)


def clear_console():
    console_text.delete("1.0", tk.END)


# Initialize main window
root = TkinterDnD.Tk()
root.title("Lecture Sound Refiner")
root.geometry("500x300")

# Dark theme configuration
root.configure(bg="#2e2e2e")
text_color = "#ffffff"
highlight_color = "#3c3f41"

# Drag-and-drop label
label = tk.Label(
    root,
    text="Drag and drop an audio file here",
    bg=highlight_color,
    fg=text_color,
    font=("Arial", 16),
)
label.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

# Console output Text widget
console_text = tk.Text(
    root, wrap="word", bg="#1e1e1e", fg="white", font=("Courier", 10), state="normal"
)
console_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Redirect stdout to console_text widget
sys.stdout = ConsoleRedirector(console_text)

# Bind the label for drag-and-drop
root.drop_target_register(DND_FILES)
root.dnd_bind("<<Drop>>", on_drop)

root.resizable(False, False)

# Run the GUI
root.mainloop()
