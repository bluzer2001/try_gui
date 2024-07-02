import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from screeninfo import get_monitors
import threading
import time

# Определение коэффициента масштабирования
monitor = get_monitors()[0]
dpi = monitor.width / (monitor.width_mm / 25.4)
scaling_factor = dpi / 96  # базовое значение DPI для Tkinter

def scale_value(value):
    return int(value * scaling_factor)

# Функции для обработки нажатий кнопок
def show_comparison_options():
    clear_frame()
    lbl_title.config(text="Сделать сравнение")

    btn_have_file = create_button(frame, "У меня есть файл", have_file, tooltip="Работа с существующим файлом")
    btn_have_file.pack(side="left", padx=scale_value(10), pady=scale_value(20), ipadx=scale_value(10), ipady=scale_value(5))

    btn_create_file = create_button(frame, "Сделать файл", show_create_file_options, tooltip="Создание нового файла")
    btn_create_file.pack(side="left", padx=scale_value(10), pady=scale_value(20), ipadx=scale_value(10), ipady=scale_value(5))

    btn_back = create_back_button()
    btn_back.pack(side="left", padx=scale_value(10), pady=scale_value(20))

def have_file():
    messagebox.showinfo("Уведомление", "Функция для работы с имеющимся файлом")

def show_create_file_options():
    clear_frame()
    lbl_title.config(text="Сделать файл")

    ttk.Label(frame, text="Выберите версию", background="white", font=("Helvetica", scale_value(12))).grid(row=0, column=0, sticky='w', pady=scale_value(5))
    version_dropdown = ttk.Combobox(frame, values=["Версия 1", "Версия 2", "Версия 3"])
    version_dropdown.grid(row=0, column=1, pady=scale_value(5), padx=scale_value(10))

    ttk.Label(frame, text="Выберите подверсию", background="white", font=("Helvetica", scale_value(12))).grid(row=1, column=0, sticky='w', pady=scale_value(5))
    subversion_dropdown = ttk.Combobox(frame, values=["Подверсия 1.1", "Подверсия 1.2", "Подверсия 1.3"])
    subversion_dropdown.grid(row=1, column=1, pady=scale_value(5), padx=scale_value(10))

    ttk.Label(frame, text="Задайте дату", background="white", font=("Helvetica", scale_value(12))).grid(row=2, column=0, sticky='w', pady=scale_value(5))
    date_entry = ttk.Entry(frame)
    date_entry.grid(row=2, column=1, pady=scale_value(5), padx=scale_value(10))

    btn_submit = create_button(frame, "Создать", lambda: start_create_file_process(version_dropdown.get(), subversion_dropdown.get(), date_entry.get()), tooltip="Создать новый файл")
    btn_submit.grid(row=3, column=0, columnspan=2, pady=scale_value(20), ipadx=scale_value(10), ipady=scale_value(5))

    btn_parameters = create_special_button(frame, "Параметры", show_parameters, tooltip="Настройки параметров")
    btn_parameters.grid(row=4, column=0, columnspan=2, pady=scale_value(10), ipadx=scale_value(10), ipady=scale_value(5))

    btn_back = create_back_button()
    btn_back.grid(row=5, column=0, columnspan=2, pady=scale_value(10), ipadx=scale_value(10), ipady=scale_value(5))

def start_create_file_process(version, subversion, date):
    # Создаем окно статуса
    status_window = tk.Toplevel(root)
    status_window.title("Статус выполнения")
    status_window.geometry("300x100")
    status_window.configure(bg="white")

    lbl_status = ttk.Label(status_window, text="Начало выполнения...", font=("Helvetica", scale_value(12)), background="white")
    lbl_status.pack(pady=scale_value(20))

    def update_status(message):
        lbl_status.config(text=message)
        status_window.update_idletasks()

    def create_file():
        update_status("Идет создание файла...")
        time.sleep(2)  # Замените это время реальной логикой выполнения

        update_status("Создание файла завершено!")
        time.sleep(1)  # Небольшая задержка, чтобы пользователь успел увидеть сообщение

        status_window.destroy()  # Закрываем окно статуса
        show_comparison_options()  # Возвращаемся к выбору после создания файла

    threading.Thread(target=create_file).start()  # Выполняем в отдельном потоке

def export_from_db():
    messagebox.showinfo("Уведомление", "Выгрузка файла из БД")

def export_from_services():
    messagebox.showinfo("Уведомление", "Выгрузка файла с сервисов")

def show_main_menu():
    clear_frame()
    lbl_title.config(text="Главное меню")

    btn_compare = create_button(frame, "Сделать сравнение", show_comparison_options, tooltip="Перейти к сравнению")
    btn_compare.pack(side="left", padx=scale_value(10), pady=scale_value(20), ipadx=scale_value(10), ipady=scale_value(5))

    btn_export_db = create_button(frame, "Выгрузить файл (из БД)", export_from_db, tooltip="Выгрузить файл из базы данных")
    btn_export_db.pack(side="left", padx=scale_value(10), pady=scale_value(20), ipadx=scale_value(10), ipady=scale_value(5))

    btn_export_services = create_button(frame, "Выгрузить файл (с сервисов)", export_from_services, tooltip="Выгрузить файл с сервисов")
    btn_export_services.pack(side="left", padx=scale_value(10), pady=scale_value(20), ipadx=scale_value(10), ipady=scale_value(5))

def show_parameters():
    messagebox.showinfo("Параметры", "Настройки параметров")

def clear_frame():
    for widget in frame.winfo_children():
        widget.destroy()

def create_button(parent, text, command, tooltip=None):
    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", scale_value(12), "bold"), background="#4CAF50", foreground="white", borderwidth=5, relief="flat", padding=(scale_value(10), scale_value(5)))
    style.map("TButton", background=[("active", "#45a049")], foreground=[("disabled", "grey")])
    button = ttk.Button(parent, text=text, command=command, style="TButton")
    if tooltip:
        create_tooltip(button, tooltip)
    return button

def create_special_button(parent, text, command, tooltip=None):
    style = ttk.Style()
    style.configure("Special.TButton", font=("Helvetica", scale_value(14), "bold"), background="#FF5722", foreground="white", borderwidth=5, relief="flat", padding=(scale_value(12), scale_value(7)))
    style.map("Special.TButton", background=[("active", "#E64A19")], foreground=[("disabled", "grey")])
    button = ttk.Button(parent, text=text, command=command, style="Special.TButton")
    if tooltip:
        create_tooltip(button, tooltip)
    return button

def create_back_button():
    back_icon = tk.PhotoImage(file="/mnt/data/Снимок экрана 2024-06-24 115010.png")  # Убедитесь, что путь правильный
    button = ttk.Button(frame, image=back_icon, command=show_main_menu, style="TButton", padding=0)
    button.image = back_icon  # Храните ссылку на изображение
    return button

def create_tooltip(widget, text):
    tooltip = ttk.Label(widget, text=text, relief="solid", borderwidth=1, background="lightyellow")
    def on_enter(event):
        tooltip.place(x=event.x_root - widget.winfo_rootx() + 20, y=event.y_rooty - widget.winfo_rooty() - 10)
    def on_leave(event):
        tooltip.place_forget()
    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)

# Основное окно
root = tk.Tk()
root.title("Главное окно")
root.state('zoomed')  # Окно будет растянуто на весь экран, но не полноэкранное
root.configure(bg="white")

lbl_title = ttk.Label(root, text="Главное меню", font=("Helvetica", scale_value(16), "bold"), background="white", foreground="#4CAF50")
lbl_title.pack(pady=scale_value(10))

logo_placeholder = ttk.Label(root, background="white")
logo_placeholder.pack(pady=scale_value(20))

frame = ttk.Frame(root, style="TFrame", padding=scale_value(20), relief="flat")
frame.pack(pady=scale_value(20))

show_main_menu()

root.mainloop()
