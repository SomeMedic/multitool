import folium
import tkinter as tk
from tkinter import messagebox
import webbrowser
import pyperclip  # Импортируем модуль pyperclip


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


root = tk.Tk()
root.title("Отображение карты")

label = tk.Label(root, text="Введите координаты: ")
label.pack()
entry = tk.Entry(root)
entry.pack()

show_button = tk.Button(root, text="Показать карту", command=show_map)
show_button.pack()

root.mainloop()
