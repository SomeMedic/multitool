import tkinter as tk
from tkinter import filedialog, ttk
from rembg import remove
from PIL import Image
import os
import time
import threading


def process_images():
    file_paths = filedialog.askopenfilenames(
        title="Select image files",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.tiff;*.webp")],
    )

    if not file_paths:
        print("No files selected. Exiting.")
        return

    for file_path in file_paths:
        process_image(file_path)


def process_image(file_path):
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()

    output_path = filedialog.asksaveasfilename(
        title="Save file to...",
        defaultextension=".png",
        filetypes=[("PNG Files", "*.png")],
    )

    if not output_path:
        return

    input_image = Image.open(file_path)

    if input_image.mode != "RGBA":
        input_image = input_image.convert("RGBA")

    processing_thread = threading.Thread(
        target=process_image_thread, args=(input_image, output_path)
    )
    processing_thread.start()


def process_image_thread(input_image, output_path):
    output_image = remove(input_image)

    for _ in range(50):
        time.sleep(0.1)
        progress_bar.step(2)

    output_image.save(output_path, format="PNG")
    print(f"Image saved to {output_path}")

    completion_label.config(text="Удаление фона завершено!")


root = tk.Tk()


root.geometry("1280x720")

root.title("Image Background Remover")


canvas = tk.Canvas(root, width=1280, height=720, highlightthickness=0)
canvas.grid(row=0, column=0)


frame = tk.Frame(canvas, padx=10, pady=10, bg=None)
frame.grid(row=0, column=0, sticky="nsew")


center_frame = tk.Frame(frame)
center_frame.grid(row=0, column=0)


title_font = ("Helvetica", 20, "bold")
title_label = tk.Label(
    center_frame, text="Background Remover", fg="#000000", font=title_font
)
title_label.grid(row=0, column=0, padx=10, pady=(20, 10))


button_font = ("Helvetica", 14, "bold")
process_button = tk.Button(
    center_frame,
    text="Загрузить изображение",
    command=process_images,
    bg="#2c3e50",
    fg="#FFFFFF",
    font=button_font,
    width=20,
    height=2,
)
process_button.grid(row=1, column=0, padx=10, pady=10)


progress_bar = ttk.Progressbar(
    center_frame, orient="horizontal", length=200, mode="determinate"
)
progress_bar.grid(row=2, column=0, padx=10, pady=10)


completion_label = tk.Label(center_frame, text="", font=("Helvetica", 12, "bold"))
completion_label.grid(row=3, column=0, padx=10, pady=10)


root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)
center_frame.grid_rowconfigure(0, weight=1)
center_frame.grid_columnconfigure(0, weight=1)

root.mainloop()
