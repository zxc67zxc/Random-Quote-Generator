import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

# Предопределённые цитаты
quotes = [
    {"text": "Знание — сила", "author": "Фрэнсис Бэкон", "topic": "Философия"},
    {"text": "Быть или не быть — вот в чём вопрос", "author": "Уильям Шекспир", "topic": "Литература"},
    {"text": "Программирование — это искусство", "author": "Мартин Фаулер", "topic": "Программирование"},
    {"text": "Успех — это способность идти от неудачи к неудаче", "author": "Уинстон Черчилль", "topic": "Мотивация"}
]

class QuoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор цитат")
        self.history = []
        self.load_history()
        self.create_widgets()
        self.setup_filters()

    def create_widgets(self):
        ttk.Button(self.root, text="Сгенерировать цитату", command=self.generate_quote).pack(pady=10)
        self.quote_label = ttk.Label(self.root, text="", wraplength=400, justify="center")
        self.quote_label.pack(pady=10)
        self.history_listbox = tk.Listbox(self.root, width=60, height=10)
        self.history_listbox.pack(pady=10)

    def setup_filters(self):
        ttk.Label(self.root, text="Фильтр по автору:").pack()
        self.author_var = tk.StringVar()
        self.author_filter = ttk.Combobox(self.root, textvariable=self.author_var, values=["Все"] + list(set(q["author"] for q in quotes)))
        self.author_filter.set("Все")
        self.author_filter.pack(pady=5)
        ttk.Label(self.root, text="Фильтр по теме:").pack()
        self.topic_var = tk.StringVar()
        self.topic_filter = ttk.Combobox(self.root, textvariable=self.topic_var, values=["Все"] + list(set(q["topic"] for q in quotes)))
        self.topic_filter.set("Все")
        self.topic_filter.pack(pady=5)
        ttk.Button(self.root, text="Применить фильтры", command=self.apply_filters).pack(pady=5)
