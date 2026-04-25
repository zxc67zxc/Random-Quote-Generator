import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime

class QuoteGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Quote Generator")
        self.root.geometry("700x600")
        
        # Предопределённые цитаты
        self.default_quotes = [
            {"text": "Будь изменением, которое ты хочешь увидеть в мире.", "author": "Махатма Ганди", "topic": "Мотивация"},
            {"text": "Жизнь — это то, что с тобой происходит, пока ты строишь планы.", "author": "Джон Леннон", "topic": "Жизнь"},
            {"text": "Самая большая слава — не в том, чтобы никогда не падать, а в том, чтобы подниматься каждый раз.", "author": "Конфуций", "topic": "Успех"},
            {"text": "Два самых важных дня в твоей жизни: день, когда ты родился, и день, когда понял зачем.", "author": "Марк Твен", "topic": "Смысл"},
            {"text": "Будущее зависит от того, что ты делаешь сегодня.", "author": "Махатма Ганди", "topic": "Мотивация"},
            {"text": "Не судите о моём успехе по моим достижениям, судите по тому, сколько раз я падал и вставал.", "author": "Нельсон Мандела", "topic": "Успех"},
        ]
        
        # Загрузка истории
        self.history_file = "quotes.json"
        self.load_history()
        
        # Создание GUI
        self.create_widgets()
        
        # Обновление фильтров
        self.update_filters()
        
    def create_widgets(self):
        # ===== Фрейм для отображения цитаты =====
        self.quote_frame = tk.LabelFrame(self.root, text="Текущая цитата", padx=10, pady=10)
        self.quote_frame.pack(fill="both", padx=10, pady=5)
        
        self.quote_label = tk.Label(self.quote_frame, text="Нажмите 'Сгенерировать'", 
                                    font=("Arial", 12, "italic"), wraplength=650)
        self.quote_label.pack()
        
        self.author_label = tk.Label(self.quote_frame, text="", font=("Arial", 10, "bold"))
        self.author_label.pack()
        
        # ===== Кнопка генерации =====
        self.generate_btn = tk.Button(self.root, text="🎲 Сгенерировать цитату", 
                                      command=self.generate_quote, bg="lightblue", font=("Arial", 11))
        self.generate_btn.pack(pady=10)
        
        # ===== Фрейм фильтрации =====
        self.filter_frame = tk.LabelFrame(self.root, text="Фильтрация", padx=10, pady=5)
        self.filter_frame.pack(fill="x", padx=10, pady=5)
        
        # Фильтр по автору
        tk.Label(self.filter_frame, text="Автор:").grid(row=0, column=0, padx=5)
        self.author_filter = ttk.Combobox(self.filter_frame, width=25)
        self.author_filter.grid(row=0, column=1, padx=5)
        self.author_filter.bind("<<ComboboxSelected>>", self.apply_filters)
        
        # Фильтр по теме
        tk.Label(self.filter_frame, text="Тема:").grid(row=0, column=2, padx=5)
        self.topic_filter = ttk.Combobox(self.filter_frame, width=25)
        self.topic_filter.grid(row=0, column=3, padx=5)
        self.topic_filter.bind("<<ComboboxSelected>>", self.apply_filters)
        
        # Кнопка сброса фильтров
        self.reset_btn = tk.Button(self.filter_frame, text="Сбросить фильтры", 
                                   command=self.reset_filters)
        self.reset_btn.grid(row=0, column=4, padx=10)
        
        # ===== История цитат =====
        self.history_frame = tk.LabelFrame(self.root, text="История цитат", padx=10, pady=5)
        self.history_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Список с прокруткой
        scrollbar = tk.Scrollbar(self.history_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_listbox = tk.Listbox(self.history_frame, yscrollcommand=scrollbar.set, 
                                          height=15, font=("Arial", 9))
        self.history_listbox.pack(fill="both", expand=True)
        scrollbar.config(command=self.history_listbox.yview)
        
        # ===== Добавление новой цитаты =====
        self.add_frame = tk.LabelFrame(self.root, text="Добавить новую цитату", padx=10, pady=5)
        self.add_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(self.add_frame, text="Цитата:").grid(row=0, column=0, sticky="e")
        self.new_quote_entry = tk.Entry(self.add_frame, width=50)
        self.new_quote_entry.grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(self.add_frame, text="Автор:").grid(row=1, column=0, sticky="e")
        self.new_author_entry = tk.Entry(self.add_frame, width=30)
        self.new_author_entry.grid(row=1, column=1, padx=5, pady=2, sticky="w")
        
        tk.Label(self.add_frame, text="Тема:").grid(row=2, column=0, sticky="e")
        self.new_topic_entry = tk.Entry(self.add_frame, width=20)
        self.new_topic_entry.grid(row=2, column=1, padx=5, pady=2, sticky="w")
        
        self.add_btn = tk.Button(self.add_frame, text="➕ Добавить цитату", 
                                 command=self.add_quote, bg="lightgreen")
        self.add_btn.grid(row=3, column=1, pady=5, sticky="w")
        
        # Обновить отображение истории
        self.refresh_history_display()
        
    def load_history(self):
        """Загрузка истории из JSON"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.quotes_history = data.get("quotes", [])
                    self.all_quotes = data.get("available_quotes", self.default_quotes.copy())
            except:
                self.quotes_history = []
                self.all_quotes = self.default_quotes.copy()
        else:
            self.quotes_history = []
            self.all_quotes = self.default_quotes.copy()
    
    def save_history(self):
        """Сохранение истории в JSON"""
        data = {
            "quotes": self.quotes_history,
            "available_quotes": self.all_quotes
        }
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def update_filters(self):
        """Обновление списков фильтров"""
        authors = sorted(set(quote["author"] for quote in self.all_quotes))
        topics = sorted(set(quote["topic"] for quote in self.all_quotes))
        
        self.author_filter['values'] = ["Все"] + authors
        self.topic_filter['values'] = ["Все"] + topics
        
        if not self.author_filter.get():
            self.author_filter.set("Все")
        if not self.topic_filter.get():
            self.topic_filter.set("Все")
    
    def get_filtered_quotes(self):
        """Получение отфильтрованных цитат"""
        author = self.author_filter.get()
        topic = self.topic_filter.get()
        
        filtered = self.all_quotes.copy()
        
        if author and author != "Все":
            filtered = [q for q in filtered if q["author"] == author]
        if topic and topic != "Все":
            filtered = [q for q in filtered if q["topic"] == topic]
        
        return filtered
    
    def generate_quote(self):
        """Генерация случайной цитаты с учётом фильтров"""
        filtered = self.get_filtered_quotes()
        
        if not filtered:
            messagebox.showwarning("Нет цитат", "Нет цитат, соответствующих выбранным фильтрам!")
            return
        
        quote = random.choice(filtered)
        
        # Отображение
        self.quote_label.config(text=f"\"{quote['text']}\"")
        self.author_label.config(text=f"— {quote['author']} (Тема: {quote['topic']})")
        
        # Добавление в историю с временной меткой
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        history_entry = {
            "timestamp": timestamp,
            "text": quote['text'],
            "author": quote['author'],
            "topic": quote['topic']
        }
        self.quotes_history.append(history_entry)
        self.save_history()
        self.refresh_history_display()
    
    def refresh_history_display(self):
        """Обновление отображения истории"""
        self.history_listbox.delete(0, tk.END)
        for entry in reversed(self.quotes_history):  # Показываем последние сверху
            display = f"[{entry['timestamp']}] {entry['author']}: \"{entry['text'][:60]}...\""
            self.history_listbox.insert(tk.END, display)
    
    def apply_filters(self, event=None):
        """Применение фильтров (при изменении)"""
        # Просто обновляем, не генерируя новую цитату
        pass
    
    def reset_filters(self):
        """Сброс фильтров"""
        self.author_filter.set("Все")
        self.topic_filter.set("Все")
        messagebox.showinfo("Фильтры сброшены", "Фильтры были сброшены")
    
    def add_quote(self):
        """Добавление новой цитаты"""
        text = self.new_quote_entry.get().strip()
        author = self.new_author_entry.get().strip()
        topic = self.new_topic_entry.get().strip()
        
        # Проверка на пустые строки
        if not text:
            messagebox.showerror("Ошибка", "Цитата не может быть пустой!")
            return
        if not author:
            messagebox.showerror("Ошибка", "Автор не может быть пустым!")
            return
        if not topic:
            messagebox.showerror("Ошибка", "Тема не может быть пустой!")
            return
        
        # Добавление
        new_quote = {
            "text": text,
            "author": author,
            "topic": topic
        }
        self.all_quotes.append(new_quote)
        self.save_history()
        
        # Очистка полей
        self.new_quote_entry.delete(0, tk.END)
        self.new_author_entry.delete(0, tk.END)
        self.new_topic_entry.delete(0, tk.END)
        
        # Обновление фильтров
        self.update_filters()
        
        messagebox.showinfo("Успех", "Цитата успешно добавлена!")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteGenerator(root)
    root.mainloop()
