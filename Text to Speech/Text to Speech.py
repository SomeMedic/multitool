import tkinter as tk
from tkinter import ttk
from tkinter import filedialog  # Добавлен импорт модуля filedialog
from gtts import gTTS
from tkinter import messagebox
import threading
import time


def convert_to_audio():
    text = text_entry.get("1.0", "end-1c")
    language = language_combo.get()

    if not text:
        messagebox.showerror("Ошибка", "Введите текст для озвучивания.")
        return

    # Очистить предыдущий прогресс, если есть
    progress_bar["value"] = 0

    def audio_conversion_thread():
        try:
            sp = gTTS(text=text, lang=language, slow=False)

            # Диалоговое окно выбора пути сохранения
            file_path = filedialog.asksaveasfilename(defaultextension=".mp3",
                                                     filetypes=[("Audio Files", "*.mp3")],
                                                     title="Сохранить аудио как")

            if not file_path:
                return  # Пользователь отменил выбор пути

            sp.save(file_path)
            messagebox.showinfo("Готово", f"Аудио сохранено в файле: {file_path}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")

        # Сбросить прогресс и сделать его невидимым
        progress_bar["value"] = 0

    audio_thread = threading.Thread(target=audio_conversion_thread)
    audio_thread.start()

    # Установить время заполнения прогресс-бара в 21 секунду
    update_progress(21)


def update_progress(total_seconds):
    # Количество обновлений прогресс-бара в секунду
    updates_per_second = 100

    # Общее количество обновлений
    total_updates = total_seconds * updates_per_second

    for i in range(total_updates + 1):
        progress = (i / total_updates) * 100
        progress_bar["value"] = progress
        app.update_idletasks()  # Обновляем GUI
        time.sleep(1 / updates_per_second)


def on_paste(event=None):
    text = app.clipboard_get()
    text_entry.delete("1.0", "end-1c")
    text_entry.insert("1.0", text)


app = tk.Tk()
app.title("Text to Speech Converter")

frame = ttk.Frame(app)
frame.grid(row=0, column=0, padx=10, pady=10)

text_label = ttk.Label(frame, text="Введите текст:")
text_label.grid(row=0, column=0, sticky="w")

text_entry = tk.Text(frame, wrap=tk.WORD, width=40, height=5)
text_entry.grid(row=1, column=0, padx=5, pady=5)

paste_button = ttk.Button(frame, text="Вставить текст", command=on_paste)
paste_button.grid(row=2, column=0, padx=5, pady=5)

language_label = ttk.Label(frame, text="Выберите язык:")
language_label.grid(row=3, column=0, sticky="w")

language_combo = ttk.Combobox(frame, values=["ru", "en"])
language_combo.grid(row=4, column=0, padx=5, pady=5)
language_combo.set("ru")

convert_button = ttk.Button(frame, text="Преобразовать в аудио", command=convert_to_audio)
convert_button.grid(row=5, column=0, padx=5, pady=5)

progress_bar = ttk.Progressbar(frame, mode='determinate', length=200)
progress_bar.grid(row=6, column=0, padx=5, pady=5)

app.mainloop()
