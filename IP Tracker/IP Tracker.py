import socket
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk

# Функция для получения IP-адреса сайта
def get_ip_address():
    try:
        target = website_entry.get()
        ip_address = socket.gethostbyname(target)
        result_label.config(text=f"IP адрес сайта {target}: {ip_address}")
    except Exception as e:
        messagebox.showerror("Ошибка", "Не удалось получить IP-адрес сайта. Проверьте введенный адрес.")

# Функция для копирования IP-адреса в буфер обмена
def copy_ip():
    ip_address = result_label.cget("text")
    if ip_address:
        root.clipboard_clear()
        root.clipboard_append(ip_address)
        root.update()

# Создаем главное окно
root = tk.Tk()
root.title("Получение IP-адреса сайта")

# Создаем метку и поле ввода для адреса сайта
website_label = tk.Label(root, text="Введите адрес сайта:")
website_label.pack()
website_entry = tk.Entry(root)
website_entry.pack()

# Создаем кнопку "Получить IP"
get_ip_button = tk.Button(root, text="Получить IP", command=get_ip_address)
get_ip_button.pack()

# Создаем метку для отображения результата
result_label = tk.Label(root, text="")
result_label.pack()

# Создаем кнопку "Копировать IP"
copy_ip_button = ttk.Button(root, text="Копировать IP", command=copy_ip)
copy_ip_button.pack()

# Запускаем главное окно
root.mainloop()
