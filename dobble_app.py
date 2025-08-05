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

# Создаем главное окно приложения
root = tk.Tk()
# 0. Заголовок Dobble
root.title("Dobble")

# Создаем виджет Canvas для рисования
canvas_width = 600
canvas_height = 300
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
canvas.pack()

# Задаем параметры для кругов
circle_radius = 100
circle_y = canvas_height / 2

# 1. Два круга, один слева, другой справа
left_circle_center_x = canvas_width / 4
right_circle_center_x = (canvas_width / 4) * 3

# 2. В левом круге цифры 1, 2, 3, 4
left_numbers = [1, 2, 3, 4]
create_circle_with_numbers(
    canvas, left_circle_center_x, circle_y, circle_radius, left_numbers
)

# 3. В правом круге цифры 4, 5, 6, 7
right_numbers = [4, 5, 6, 7]
create_circle_with_numbers(
    canvas, right_circle_center_x, circle_y, circle_radius, right_numbers
)

# Запускаем главный цикл обработки событий
root.mainloop()
