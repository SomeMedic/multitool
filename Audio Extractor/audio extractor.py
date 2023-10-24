import moviepy.editor
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

video_path = filedialog.askopenfilename(title="Выберите видеофайл")

audio_path = filedialog.asksaveasfilename(title="Сохранить аудиофайл как", defaultextension=".mp3", filetypes=[("MP3 Files", "*.mp3")])

try:
    video_extension = video_path.split(".")[-1].lower()

    if video_extension != "mp4":
        converted_video_path = "converted_video.mp4"
        video = moviepy.editor.VideoFileClip(video_path)
        video.write_videofile(converted_video_path, codec='libx264')
    else:
        converted_video_path = video_path

    video = moviepy.editor.VideoFileClip(converted_video_path)
    audio = video.audio
    audio.write_audiofile(audio_path)
    print("Аудио успешно извлечено и сохранено.")
except Exception as e:
    print(f"Произошла ошибка: {str(e)}")
