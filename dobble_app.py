
import tkinter as tk
import math
import time

def create_circle_with_numbers(canvas, center_x, center_y, radius, numbers, tag_prefix):
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
        # Добавляем тег для идентификации
        canvas.create_text(x, y, text=str(number), font=font, tags=(f"{tag_prefix}_{number}", "number"))



# --- Основная часть программы ---


# --- Dobble Game State ---
class DobbleGame:
    def __init__(self, root, canvas):
        self.root = root
        self.canvas = canvas
        self.score = 0
        self.time_left = 15  # 15 секунд
        self.timer_id = None
        self.start_time = time.time()
        self.left_numbers = [1, 2, 3, 4]
        self.right_numbers = [4, 5, 6, 7]
        self.common = list(set(self.left_numbers) & set(self.right_numbers))
        self.score_label = tk.Label(root, text=f"Очки: {self.score}", font=("Arial", 14))
        self.score_label.pack()
        self.timer_label = tk.Label(root, text=f"Время: {self.time_left}", font=("Arial", 14))
        self.timer_label.pack()
        self.draw_circles()
        self.bind_numbers()
        self.update_timer()

    def draw_circles(self):
        self.canvas.delete("all")
        create_circle_with_numbers(self.canvas, left_circle_center_x, circle_y, circle_radius, self.left_numbers, "left")
        create_circle_with_numbers(self.canvas, right_circle_center_x, circle_y, circle_radius, self.right_numbers, "right")

    def bind_numbers(self):
        # Привязываем обработчик ко всем цифрам
        for number in set(self.left_numbers + self.right_numbers):
            self.canvas.tag_bind(f"left_{number}", "<Button-1>", lambda e, n=number: self.on_number_click(n))
            self.canvas.tag_bind(f"right_{number}", "<Button-1>", lambda e, n=number: self.on_number_click(n))

    def on_number_click(self, number):
        if number in self.common:
            self.score += 10
            self.score_label.config(text=f"Очки: {self.score}")
            # Можно добавить смену карточек или анимацию
        else:
            self.end_game(wrong=True)

    def update_timer(self):
        self.timer_label.config(text=f"Время: {self.time_left}")
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.end_game()

    def end_game(self, wrong=False):
        self.canvas.unbind("<Button-1>")
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        if wrong:
            msg = f"Неправильный ответ! Итог: {self.score}"
            color = "orange"
        else:
            msg = f"Время вышло! Итог: {self.score}"
            color = "red"
        self.canvas.create_text(canvas_width/2, canvas_height/2, text=msg, font=("Arial", 24), fill=color)


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
left_circle_center_x = canvas_width / 4
right_circle_center_x = (canvas_width / 4) * 3

# Запускаем игру
game = DobbleGame(root, canvas)

# Запускаем главный цикл обработки событий
root.mainloop()
