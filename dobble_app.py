import tkinter as tk
import math
import random
import string

def create_circle_with_symbols(canvas, center_x, center_y, radius, symbols):
    """
    Рисует круг на холсте и размещает в нем символы,
    распределяя их равномерно по окружности с разными размерами шрифта.
    """
    # Рисуем контур круга
    canvas.create_oval(
        center_x - radius, center_y - radius,
        center_x + radius, center_y + radius,
        outline="black", width=2
    )

    # Рассчитываем позиции и рисуем символы
    num_count = len(symbols)
    text_radius = radius * 0.75  # Размещаем символы ближе к краю
    
    # Распределяем символы равномерно, начиная сверху (угол -90 градусов)
    angle_increment = 360 / num_count
    start_angle = -90

    for i, symbol in enumerate(symbols):
        angle = math.radians(start_angle + i * angle_increment)
        x = center_x + text_radius * math.cos(angle)
        y = center_y + text_radius * math.sin(angle)
        
        # Разный размер шрифта для каждого символа (от 16 до 22)
        font_size = random.randint(16, 22)
        font = ("Arial", font_size, "bold")
        
        # Ресуем символы
        canvas.create_text(x, y, text=symbol, font=font)

def generate_random_symbols(count, common_symbol):
    """Генерирует список случайных букв с заданным общим символом"""
    symbols = set()
    
    # Добавляем уникальные буквы, пока не достигнем нужного количества
    while len(symbols) < count - 1:
        symbol = random.choice(string.ascii_uppercase)
        if symbol != common_symbol and symbol not in used_symbols:
            symbols.add(symbol)
            used_symbols.add(symbol)
    
    result = list(symbols)
    result.append(common_symbol)
    random.shuffle(result)
    return result

# --- Основная часть программы ---

root = tk.Tk()
root.title("Dobble с символами")

canvas_width = 900  # Увеличили ширину холста
canvas_height = 500
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
canvas.pack(pady=20)

# Параметры кругов
circle_radius = 160
circle_y = canvas_height / 2

# Позиции кругов (увеличили расстояние между центрами)
left_circle_center_x = canvas_width / 4
right_circle_center_x = (canvas_width / 4) * 3

# Глобальная переменная для общего символа
common_symbol = random.choice(string.ascii_uppercase)
used_symbols = {common_symbol}  # Множество для отслеживания использованных символов

# Генерируем случайные символы с одним общим
symbols_per_circle = 8
left_symbols = generate_random_symbols(symbols_per_circle, common_symbol)
right_symbols = generate_random_symbols(symbols_per_circle, common_symbol)

# Создаем круги с символами
create_circle_with_symbols(
    canvas, left_circle_center_x, circle_y, circle_radius, left_symbols
)

create_circle_with_symbols(
    canvas, right_circle_center_x, circle_y, circle_radius, right_symbols
)

# Добавляем подсказку
canvas.create_text(
    canvas_width/2, 30,
    text=f"Найдите общий символ!",
    font=("Arial", 18, "bold"),
    fill="blue"
)

# Проверка, что совпадение только одно (для отладки)
intersection = set(left_symbols) & set(right_symbols)
print(f"Общий символ: {common_symbol}, совпадений: {intersection}")

root.mainloop()