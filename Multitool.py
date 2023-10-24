import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import moviepy.editor as mp
from PIL import Image
import os
import time
import threading
import socket
import webbrowser
import pyperclip
import folium
from gtts import gTTS
from io import BytesIO
import pygame
import tempfile
from rembg import remove

def extract_audio():
    video_path = filedialog.askopenfilename(
        title="Выберите видеофайл",
        filetypes=[("Video Files", "*.mp4;*.avi;*.mkv;*.mov")]
    )

    if not video_path:
        return

    audio_path = filedialog.asksaveasfilename(
        title="Сохранить аудиофайл как",
        defaultextension=".mp3",
        filetypes=[("MP3 Files", "*.mp3")]
    )

    try:
        video_extension = video_path.split(".")[-1].lower()

        if video_extension != "mp4":
            converted_video_path = "converted_video.mp4"
            video = mp.VideoFileClip(video_path)
            video.write_videofile(converted_video_path, codec='libx264')
        else:
            converted_video_path = video_path

        video = mp.VideoFileClip(converted_video_path)
        audio = video.audio
        audio.write_audiofile(audio_path)
        print("Аудио успешно извлечено и сохранено.")
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")

def process_images():
    file_paths = filedialog.askopenfilenames(
        title="Выберите изображения",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.tiff;*.webp")]
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
        title="Сохранить файл как...",
        defaultextension=".png",
        filetypes=[("PNG Files", "*.png")]
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

def get_ip_address():
    try:
        target = website_entry.get()
        ip_address = socket.gethostbyname(target)
        result_label.config(text=f"IP адрес сайта {target}: {ip_address}")
    except Exception as e:
        messagebox.showerror("Ошибка", "Не удалось получить IP-адрес сайта. Проверьте введенный адрес.")

def copy_ip():
    ip_address = result_label.cget("text")
    if ip_address:
        root.clipboard_clear()
        root.clipboard_append(ip_address)
        root.update()

def show_map():
    try:
        clipboard_text = pyperclip.paste()
        coordinates = clipboard_text.split(',')
        lat, lon = float(coordinates[0]), float(coordinates[1])

        place = folium.Map(location=[lat, lon], zoom_start=15)
        folium.Marker([lat, lon], tooltip='Ваша точка').add_to(place)

        place.save("temp_map.html")
        webbrowser.open("temp_map.html")

    except Exception as e:
        messagebox.showerror("Ошибка",
                             "Некорректные координаты. Пожалуйста, вставьте их в формате 'широта, долгота' из буфера обмена (Ctrl+V).")

def convert_to_audio():
    text = text_entry.get("1.0", "end-1c")
    language = language_combo.get()

    if not text:
        messagebox.showerror("Ошибка", "Введите текст для озвучивания.")
        return

    progress_bar["value"] = 0

    def audio_conversion_thread():
        try:
            sp = gTTS(text=text, lang=language, slow=False)

            file_path = filedialog.asksaveasfilename(defaultextension=".mp3",
                                                     filetypes=[("Audio Files", "*.mp3")],
                                                     title="Сохранить аудио как")

            if not file_path:
                return

            sp.save(file_path)
            messagebox.showinfo("Готово", f"Аудио сохранено в файле: {file_path}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")

        progress_bar["value"] = 0

    audio_thread = threading.Thread(target=audio_conversion_thread)
    audio_thread.start()

    update_progress(21)

def update_progress(total_seconds):
    updates_per_second = 100
    total_updates = total_seconds * updates_per_second

    for i in range(total_updates + 1):
        progress = (i / total_updates) * 100
        progress_bar["value"] = progress
        app.update_idletasks()
        time.sleep(1 / updates_per_second)

def on_paste(event=None):
    text = app.clipboard_get()
    text_entry.delete("1.0", "end-1c")
    text_entry.insert("1.0", text)

app = tk.Tk()
app.title("Мультитул приложение")

main_window = ttk.Notebook(app)
main_window.pack(padx=10, pady=10)

audio_tab = ttk.Frame(main_window)
main_window.add(audio_tab, text="Извлечение аудио из видео")

audio_label = tk.Label(audio_tab, text="Извлечение аудио из видео", font=("Helvetica", 20, "bold"))
audio_label.pack(pady=20)

audio_button = tk.Button(
    audio_tab,
    text="Выберите видеофайл и извлеките аудио",
    command=extract_audio,
    bg="#2c3e50",
    fg="#FFFFFF",
    font=("Helvetica", 14, "bold"),
    width=40,
    height=2,
)
audio_button.pack(pady=20)

image_tab = ttk.Frame(main_window)
main_window.add(image_tab, text="Удаление фона из изображений")

image_label = tk.Label(image_tab, text="Удаление фона из изображений", font=("Helvetica", 20, "bold"))
image_label.pack(pady=20)

image_button = tk.Button(
    image_tab,
    text="Выберите изображения и удалите фон",
    command=process_images,
    bg="#2c3e50",
    fg="#FFFFFF",
    font=("Helvetica", 14, "bold"),
    width=40,
    height=2,
)
image_button.pack(pady=20)

ip_tab = ttk.Frame(main_window)
main_window.add(ip_tab, text="Получение IP адреса")

ip_label = tk.Label(ip_tab, text="Получение IP адреса сайта", font=("Helvetica", 20, "bold"))
ip_label.pack(pady=20)

website_label = tk.Label(ip_tab, text="Введите адрес сайта:")
website_label.pack()

website_entry = tk.Entry(ip_tab)
website_entry.pack()

get_ip_button = tk.Button(ip_tab, text="Получить IP", command=get_ip_address)
get_ip_button.pack(pady=10)

result_label = tk.Label(ip_tab, text="")
result_label.pack(pady=10)

copy_ip_button = ttk.Button(ip_tab, text="Копировать IP", command=copy_ip)
copy_ip_button.pack(pady=10)

map_tab = ttk.Frame(main_window)
main_window.add(map_tab, text="Отображение карты")

map_label = tk.Label(map_tab, text="Введите координаты (широта, долгота) или вставьте из буфера обмена:")
map_label.pack(pady=10)

map_entry = tk.Entry(map_tab)
map_entry.pack(pady=5)

show_map_button = tk.Button(map_tab, text="Показать карту", command=show_map)
show_map_button.pack(pady=10)

speech_tab = ttk.Frame(main_window)
main_window.add(speech_tab, text="Текст в речь")

speech_title_label = tk.Label(
    speech_tab, text="Преобразование текста в речь", font=("Helvetica", 20, "bold")
)
speech_title_label.pack(pady=20)

text_label = tk.Label(speech_tab, text="Введите текст:")
text_label.pack()

text_entry = tk.Text(speech_tab, height=5, width=50)
text_entry.pack(pady=10)

paste_button = ttk.Button(speech_tab, text="Вставить текст", command=on_paste)
paste_button.pack(pady=10)

language_label = ttk.Label(speech_tab, text="Выберите язык:")
language_label.pack()

language_combo = ttk.Combobox(speech_tab, values=["ru", "en"])
language_combo.pack(pady=5)
language_combo.set("ru")

convert_button = ttk.Button(speech_tab, text="Преобразовать в аудио", command=convert_to_audio)
convert_button.pack(pady=10)

progress_bar = ttk.Progressbar(speech_tab, mode='determinate', length=200)
progress_bar.pack(pady=10)

app.mainloop()
