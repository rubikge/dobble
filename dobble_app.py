import tkinter as tk
import math
import random
import string

def create_circle_with_symbols(canvas, center_x, center_y, radius, symbols, common_symbol, tag=None):
    """
    Рисует круг на холсте и размещает в нем символы,
    распределяя их равномерно по окружности с разными размерами шрифта.
    """
    # Рисуем контур круга
    canvas.create_oval(
        center_x - radius, center_y - radius,
        center_x + radius, center_y + radius,
        outline="black", width=2, tags=tag
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
        
        # Рисуем символы, выделяем общий символ красным
        if symbol == common_symbol:
            canvas.create_text(x, y, text=symbol, font=font, fill="red", tags=f"{tag}_symbol_{i}" if tag else None)
        else:
            canvas.create_text(x, y, text=symbol, font=font, tags=f"{tag}_symbol_{i}" if tag else None)

def generate_random_symbols(count, common_symbol, used_symbols):
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

def restart_game():
    """Перезапускает игру с новыми карточками"""
    global common_symbol, used_symbols, left_symbols, right_symbols
    
    # Очищаем холст
    canvas.delete("all")
    
    # Генерируем новый общий символ
    common_symbol = random.choice(string.ascii_uppercase)
    used_symbols = {common_symbol}
    
    # Создаем новые карточки
    left_symbols = generate_random_symbols(symbols_per_circle, common_symbol, used_symbols)
    right_symbols = generate_random_symbols(symbols_per_circle, common_symbol, used_symbols)
    
    # Рисуем карточки
    create_circle_with_symbols(
        canvas, left_circle_center_x, circle_y, circle_radius, 
        left_symbols, common_symbol, "left_card"
    )
    create_circle_with_symbols(
        canvas, right_circle_center_x, circle_y, circle_radius, 
        right_symbols, common_symbol, "right_card"
    )
    
    # Добавляем подсказку
    canvas.create_text(
        canvas_width/2, 30,
        text="Найдите общий символ (красный) в ЛЕВОЙ карточке и кликните по нему!",
        font=("Arial", 16, "bold"),
        fill="blue"
    )

def on_click(event):
    """Обработчик клика мыши"""
    # Находим объекты под курсором
    items = canvas.find_overlapping(event.x-1, event.y-1, event.x+1, event.y+1)
    
    for item in items:
        tags = canvas.gettags(item)
        # Проверяем, кликнули ли на символ в левой карточке
        if any(tag.startswith("left_card_symbol_") for tag in tags):
            symbol = canvas.itemcget(item, "text")
            # Если кликнули на общий символ (красный)
            if symbol == common_symbol:
                restart_game()
                break

# --- Основная часть программы ---

root = tk.Tk()
root.title("Dobble с символами")

canvas_width = 900
canvas_height = 500
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
canvas.pack(pady=20)

# Привязываем обработчик кликов
canvas.bind("<Button-1>", on_click)

# Параметры кругов
circle_radius = 160
circle_y = canvas_height / 2

# Позиции кругов
left_circle_center_x = canvas_width / 4
right_circle_center_x = (canvas_width / 4) * 3

# Настройки игры
symbols_per_circle = 8
common_symbol = None
used_symbols = set()
left_symbols = []
right_symbols = []

# Запускаем первую игру
restart_game()

root.mainloop()