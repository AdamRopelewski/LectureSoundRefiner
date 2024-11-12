import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import messagebox
import main
import os
import threading


def process_audio(file_path):
    # Validate file extension
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
    file_path = file_path[1:-1]
    print(file_path)
    file_extension = os.path.splitext(file_path)[1].lower()
    file_extension = file_extension.replace("}", "")
    print(file_extension)
    if file_extension not in valid_extensions:
        messagebox.showerror(
            "Invalid File", "Please drop a valid audio file (e.g., .wav, .mp3, .flac)"
        )
        return

    # Set output file path in the same directory as the input file
    output_file = os.path.join(os.path.dirname(file_path), "output.mp3")

    # Run the audio processing in a separate thread
    thread = threading.Thread(
        target=run_audio_processing, args=(file_path, output_file)
    )
    thread.start()


def run_audio_processing(file_path, output_file):
    # Process the audio (replace with actual audio processing function)
    main.main(file_path, output_file)

    # Notify the user after processing is complete
    messagebox.showinfo(
        "Processing Complete", f"Processed file saved as: {output_file}"
    )


def on_drop(event):
    file_path = event.data
    process_audio(file_path)


# Initialize main window
root = TkinterDnD.Tk()  # Use TkinterDnD.Tk instead of tk.Tk to enable drag-and-drop
root.title("Lecture Sound Refiner")
root.geometry("400x200")

# Dark theme configuration
root.configure(bg="#2e2e2e")  # Dark background
text_color = "#ffffff"  # White text
highlight_color = "#3c3f41"  # Slightly lighter background for the drop area

# Set up drag-and-drop label
label = tk.Label(
    root,
    text="Drag and drop an audio file here",
    bg="lightgray",
    fg="black",
    font=("Arial", 12),
)
label.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Bind the label for drag-and-drop
root.drop_target_register(DND_FILES)
root.dnd_bind("<<Drop>>", on_drop)

root.mainloop()
