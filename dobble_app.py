import tkinter as tk
import math
import random
import string
from tkinter.font import Font

class DobbleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Dobble Game")
        
        # Настройки игры
        self.symbols_per_card = 8
        self.card_radius = 180  # Увеличил радиус круга
        self.min_distance = 45  # Увеличил минимальное расстояние между символами
        self.canvas_width = 1000
        self.canvas_height = 600
        
        # Создаем холст
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack(pady=20)
        
        # Позиции карточек
        self.left_card_center = (self.canvas_width // 4, self.canvas_height // 2)
        self.right_card_center = (3 * self.canvas_width // 4, self.canvas_height // 2)
        
        # Шрифты
        self.font_sizes = [20, 22, 24, 26]  # Увеличил размеры шрифтов
        self.fonts = [Font(family="Arial", size=s, weight="bold") for s in self.font_sizes]
        
        # Инициализация игры
        self.common_symbol = None
        self.used_symbols = set()
        self.left_card_symbols = []
        self.right_card_symbols = []
        
        # Создаем новую игру
        self.new_game()
        
        # Привязываем обработчик кликов
        self.canvas.bind("<Button-1>", self.handle_click)

    def new_game(self):
        """Инициализирует новую игру с новыми карточками"""
        self.canvas.delete("all")
        self.used_symbols = set()
        
        # Генерируем общий символ
        self.common_symbol = random.choice(string.ascii_uppercase)
        self.used_symbols.add(self.common_symbol)
        
        # Создаем левую карточку
        self.left_card_symbols = self.generate_card_symbols(self.common_symbol)
        self.draw_card(self.left_card_center, self.left_card_symbols, "left")
        
        # Создаем правую карточку
        self.right_card_symbols = self.generate_card_symbols(self.common_symbol)
        self.draw_card(self.right_card_center, self.right_card_symbols, "right")
        
        # Рисуем инструкцию
        self.draw_instructions()

    def generate_card_symbols(self, common_symbol):
        """Генерирует символы для карточки с заданным общим символом"""
        symbols = set()
        
        # Добавляем уникальные символы
        while len(symbols) < self.symbols_per_card - 1:
            symbol = random.choice(string.ascii_uppercase)
            if symbol != common_symbol and symbol not in self.used_symbols:
                symbols.add(symbol)
                self.used_symbols.add(symbol)
        
        result = list(symbols)
        result.append(common_symbol)
        random.shuffle(result)
        return result

    def is_valid_position(self, center, radius, new_pos, existing_positions, font_size):
        """Проверяет, что новая позиция допустима"""
        x, y = center
        new_x, new_y = new_pos
        
        # Проверка, что символ внутри круга (с учетом размера шрифта)
        distance_to_center = math.sqrt((new_x - x)**2 + (new_y - y)**2)
        max_distance = radius - font_size  # Учитываем размер шрифта
        if distance_to_center > max_distance:
            return False
        
        # Проверка на пересечение с другими символами (увеличил минимальное расстояние)
        for (ex_x, ex_y, ex_size) in existing_positions:
            distance = math.sqrt((new_x - ex_x)**2 + (new_y - ex_y)**2)
            min_required = (font_size + ex_size) / 2 + 15  # Увеличил дополнительное расстояние
            if distance < min_required:
                return False
                
        return True

    def draw_card(self, center, symbols, tag):
        """Рисует карточку со случайно расположенными символами"""
        x, y = center
        radius = self.card_radius
        
        # Рисуем круг карточки
        self.canvas.create_oval(
            x - radius, y - radius,
            x + radius, y + radius,
            outline="black", width=3, tags=tag
        )
        
        existing_positions = []
        max_attempts = 200  # Увеличил количество попыток
        
        for i, symbol in enumerate(symbols):
            font = random.choice(self.fonts)
            font_size = int(font['size'])
            
            # Пытаемся найти подходящую позицию
            for attempt in range(max_attempts):
                # Генерируем случайный угол и расстояние от центра
                angle = random.uniform(0, 2 * math.pi)
                # Ограничиваем максимальное расстояние с учетом размера шрифта
                max_dist = radius - font_size - 10
                distance = random.uniform(radius * 0.3, max_dist)  # Не слишком близко к центру
                
                text_x = x + distance * math.cos(angle)
                text_y = y + distance * math.sin(angle)
                
                if self.is_valid_position(center, radius, (text_x, text_y), existing_positions, font_size):
                    existing_positions.append((text_x, text_y, font_size))
                    self.canvas.create_text(
                        text_x, text_y,
                        text=symbol,
                        font=font,
                        tags=f"{tag}_symbol_{i}"
                    )
                    break
            else:
                # Если не нашли позицию после всех попыток, размещаем ближе к краю
                angle = random.uniform(0, 2 * math.pi)
                distance = radius - font_size - 5
                text_x = x + distance * math.cos(angle)
                text_y = y + distance * math.sin(angle)
                existing_positions.append((text_x, text_y, font_size))
                self.canvas.create_text(
                    text_x, text_y,
                    text=symbol,
                    font=font,
                    tags=f"{tag}_symbol_{i}"
                )

    def draw_instructions(self):
        """Рисует инструкцию для игрока"""
        self.canvas.create_text(
            self.canvas_width // 2, 30,
            text="Найдите и кликните на общий символ в ЛЕВОЙ карточке",
            font=("Arial", 16, "bold"),
            fill="blue"
        )

    def handle_click(self, event):
        """Обрабатывает клики игрока"""
        clicked_items = self.canvas.find_overlapping(event.x-5, event.y-5, event.x+5, event.y+5)
        
        for item in clicked_items:
            tags = self.canvas.gettags(item)
            if "left_symbol" in " ".join(tags):
                symbol = self.canvas.itemcget(item, "text")
                if symbol == self.common_symbol:
                    self.new_game()
                    break

# Запуск игры
if __name__ == "__main__":
    root = tk.Tk()
    game = DobbleGame(root)
    root.mainloop()