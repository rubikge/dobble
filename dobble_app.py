import tkinter as tk
import math

def create_circle_with_numbers(canvas, center_x, center_y, radius, numbers):
    """
    Рисует круг на холсте и размещает в нем числа из списка,
    распределяя их равномерно по окружности.

    Args:
        canvas (tk.Canvas): Виджет холста для рисования.
        center_x (int): Координата X центра круга.
        center_y (int): Координата Y центра круга.
        radius (int): Радиус круга.
        numbers (list): Список чисел для отображения в круге.
    """
    # Рисуем контур круга
    canvas.create_oval(
        center_x - radius, center_y - radius,
        center_x + radius, center_y + radius,
        outline="black", width=2
    )

    # Рассчитываем позиции и рисуем числа
    num_count = len(numbers)
    # Размещаем числа на воображаемом круге меньшего радиуса
    text_radius = radius * 0.7
    # "Большие" цифры - размер шрифта зависит от радиуса
    font_size = int(radius / 3)
    font = ("Arial", font_size, "bold")

    # Распределяем числа равномерно, начиная сверху (угол -90 градусов)
    angle_increment = 360 / num_count
    start_angle = -90

    for i, number in enumerate(numbers):
        angle = math.radians(start_angle + i * angle_increment)
        x = center_x + text_radius * math.cos(angle)
        y = center_y + text_radius * math.sin(angle)
        canvas.create_text(x, y, text=str(number), font=font)



# --- Основная часть программы ---

def start_game():
    start_frame.pack_forget()
    game_frame.pack(fill="both", expand=True)
    draw_game()

def draw_game():
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    canvas.delete("all")
    # Радиус круга зависит от размера окна
    circle_radius = min(canvas_width, canvas_height) // 4
    circle_y = canvas_height / 2
    left_circle_center_x = canvas_width / 4
    right_circle_center_x = (canvas_width / 4) * 3
    left_numbers = [1, 2, 3, 4]
    right_numbers = [4, 5, 6, 7]
    create_circle_with_numbers(
        canvas, left_circle_center_x, circle_y, circle_radius, left_numbers
    )
    create_circle_with_numbers(
        canvas, right_circle_center_x, circle_y, circle_radius, right_numbers
    )


# Создаем главное окно приложения
root = tk.Tk()
root.title("Dobble")

# Минимальные размеры окна (пропорции минимума окна задаются здесь)
MIN_WIDTH = 600   # минимальная ширина окна
MIN_HEIGHT = 500  # минимальная высота окна
root.minsize(MIN_WIDTH, MIN_HEIGHT)


# Стартовый экран
start_frame = tk.Frame(root, bg="#adb085")
start_frame.pack(fill="both", expand=True)

# Функция для центрирования элементов выше середины окна
def place_start_widgets():
    start_frame.update_idletasks()
    frame_height = start_frame.winfo_height()
    frame_width = start_frame.winfo_width()
    btn_height = 60  # Примерная высота кнопки Play в пикселях
    offset = frame_height // 2 - btn_height * 2
    if offset < 0:
        offset = 20
    title_label.place(relx=0.5, y=offset, anchor="s")
    play_button.place(relx=0.5, y=offset + btn_height + 10, anchor="n")

title_label = tk.Label(start_frame, text="Dobble", font=("Arial", 32, "bold"), bg="#adb085")
play_button = tk.Button(start_frame, text="Play", font=("Arial", 20), width=15, height=1, command=start_game)

# Размещаем элементы после изменения размера окна
def on_start_resize(event):
    place_start_widgets()
start_frame.bind("<Configure>", on_start_resize)

# Первоначальное размещение
place_start_widgets()


# Игровой экран (изначально скрыт)
game_frame = tk.Frame(root)
canvas = tk.Canvas(game_frame, bg="#adb085")
canvas.pack(fill="both", expand=True)

# Перерисовывать игру при изменении размера окна
def on_resize(event):
    if game_frame.winfo_ismapped():
        draw_game()
canvas.bind("<Configure>", on_resize)

# Запускаем главный цикл обработки событий
root.mainloop()
