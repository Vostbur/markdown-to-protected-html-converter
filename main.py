import tkinter as tk
from tkinter import filedialog, messagebox
import base64
import re
import sys
import os
import hashlib
import markdown2
import json
from datetime import datetime, timedelta

class MarkdownToProtectedHTMLConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Markdown to Protected HTML Converter")

        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        self.encryption_key = tk.StringVar()
        self.show_key = tk.BooleanVar(value=False)
        self.enable_timer = tk.BooleanVar(value=False)
        self.enable_limit = tk.BooleanVar(value=False)
        self.timer_hours = tk.StringVar(value="0")
        self.timer_minutes = tk.StringVar(value="0")
        self.timer_seconds = tk.StringVar(value="0")
        self.max_fragments = tk.StringVar(value="1")

        # Загрузка HTML-шаблона
        self.html_template = self.load_template(resource_path('template.html'))
        if self.html_template is None:
            messagebox.showerror("Error", "Could not load template.html")
            self.root.destroy()
            return

        self.create_widgets()

    def load_template(self, template_path):
        """Загружает HTML-шаблон из файла"""
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error loading template: {str(e)}")
            return None

    def create_widgets(self):
        file_frame = tk.LabelFrame(self.root, text="Markdown File", padx=5, pady=5)
        file_frame.pack(padx=10, pady=5, fill="x")

        tk.Label(file_frame, text="Input File:").grid(row=0, column=0, sticky="w")
        tk.Entry(file_frame, textvariable=self.input_file, width=50).grid(row=0, column=1)
        tk.Button(file_frame, text="Browse...", command=self.browse_input_file).grid(row=0, column=2)

        key_frame = tk.LabelFrame(self.root, text="Encryption Key", padx=5, pady=5)
        key_frame.pack(padx=10, pady=5, fill="x")

        tk.Label(key_frame, text="Encryption Key:").grid(row=0, column=0, sticky="w")
        self.key_entry = tk.Entry(key_frame, textvariable=self.encryption_key, show="*", width=50)
        self.key_entry.grid(row=1, column=0, columnspan=2)
        tk.Checkbutton(
            key_frame,
            text="Show key",
            variable=self.show_key,
            command=self.toggle_key_visibility
        ).grid(row=1, column=2, sticky="w")

        # Фрейм для таймера
        timer_frame = tk.LabelFrame(self.root, text="Timer Settings", padx=5, pady=5)
        timer_frame.pack(padx=10, pady=5, fill="x")

        tk.Checkbutton(
            timer_frame,
            text="Enable countdown timer",
            variable=self.enable_timer,
            command=self.toggle_timer_fields
        ).grid(row=0, column=0, columnspan=3, sticky="w")

        self.timer_fields_frame = tk.Frame(timer_frame)
        self.timer_fields_frame.grid(row=1, column=0, columnspan=3, sticky="w")

        tk.Label(self.timer_fields_frame, text="Hours:").grid(row=0, column=0)
        tk.Spinbox(self.timer_fields_frame, from_=0, to=24, textvariable=self.timer_hours, width=3).grid(row=0, column=1)

        tk.Label(self.timer_fields_frame, text="Minutes:").grid(row=0, column=2)
        tk.Spinbox(self.timer_fields_frame, from_=0, to=59, textvariable=self.timer_minutes, width=3).grid(row=0, column=3)

        tk.Label(self.timer_fields_frame, text="Seconds:").grid(row=0, column=4)
        tk.Spinbox(self.timer_fields_frame, from_=0, to=59, textvariable=self.timer_seconds, width=3).grid(row=0, column=5)

        # Фрейм для ограничения фрагментов
        limit_frame = tk.LabelFrame(self.root, text="Fragment Access Limit", padx=5, pady=5)
        limit_frame.pack(padx=10, pady=5, fill="x")

        tk.Checkbutton(
            limit_frame,
            text="Enable maximum fragments limit",
            variable=self.enable_limit,
            command=self.toggle_limit_fields
        ).grid(row=0, column=0, columnspan=3, sticky="w")

        self.limit_fields_frame = tk.Frame(limit_frame)
        self.limit_fields_frame.grid(row=1, column=0, columnspan=3, sticky="w")

        tk.Label(self.limit_fields_frame, text="Max fragments to open:").grid(row=0, column=0)
        tk.Spinbox(
            self.limit_fields_frame,
            from_=1,
            to=100,
            textvariable=self.max_fragments,
            width=5
        ).grid(row=0, column=1)

        output_frame = tk.LabelFrame(self.root, text="Output HTML File", padx=5, pady=5)
        output_frame.pack(padx=10, pady=5, fill="x")

        tk.Label(output_frame, text="Output File:").grid(row=0, column=0, sticky="w")
        tk.Entry(output_frame, textvariable=self.output_file, width=50).grid(row=0, column=1)
        tk.Button(output_frame, text="Browse...", command=self.browse_output_file).grid(row=0, column=2)

        tk.Button(
            self.root,
            text="Convert to Protected HTML",
            command=self.convert,
            bg="#4CAF50",
            fg="white"
        ).pack(pady=10)

    def toggle_key_visibility(self):
        if self.show_key.get():
            self.key_entry.config(show="")
        else:
            self.key_entry.config(show="*")

    def toggle_timer_fields(self):
        if self.enable_timer.get():
            self.timer_fields_frame.grid()
        else:
            self.timer_fields_frame.grid_remove()

    def toggle_limit_fields(self):
        """Показывает/скрывает поля для ограничения фрагментов"""
        if self.enable_limit.get():
            self.limit_fields_frame.grid()
        else:
            self.limit_fields_frame.grid_remove()

    def browse_input_file(self):
        filename = filedialog.askopenfilename(
            title="Select Markdown File",
            filetypes=(("Markdown files", "*.md"), ("All files", "*.*"))
        )
        if filename:
            self.input_file.set(filename)
            base = os.path.splitext(filename)[0]
            self.output_file.set(base + "_protected.html")

    def browse_output_file(self):
        filename = filedialog.asksaveasfilename(
            title="Save HTML File",
            defaultextension=".html",
            filetypes=(("HTML files", "*.html"), ("All files", "*.*"))
        )
        if filename:
            self.output_file.set(filename)

    def encrypt_text(self, text, key):
        text_bytes = text.encode('utf-8')
        key_bytes = key.encode('utf-8')
        encrypted_bytes = bytearray()

        for i in range(len(text_bytes)):
            encrypted_bytes.append(text_bytes[i] ^ key_bytes[i % len(key_bytes)])

        return base64.b64encode(encrypted_bytes).decode('utf-8')

    def convert(self):
        try:
            # Проверки ввода
            if not self.input_file.get():
                messagebox.showerror("Error", "Please select input Markdown file")
                return

            if not self.encryption_key.get():
                messagebox.showerror("Error", "Please enter encryption key")
                return

            key = self.encryption_key.get()
            key_hash = hashlib.sha256(key.encode()).hexdigest()

            if not self.output_file.get():
                messagebox.showerror("Error", "Please specify output HTML file")
                return

            # Чтение и обработка Markdown
            with open(self.input_file.get(), 'r', encoding='utf-8') as f:
                content = f.read()

            # Инициализация конвертера Markdown с полной поддержкой синтаксиса
            md = markdown2.Markdown(extras=["tables", "fenced-code-blocks", "cuddled-lists"])

            # Обработка скрытых фрагментов
            hints = []
            def process_hint(match):
                hint_content = match.group(1).strip()
                # Конвертируем Markdown в HTML перед шифрованием
                hint_html = md.convert(hint_content)
                encrypted = self.encrypt_text(hint_html, key)
                hints.append(encrypted)
                return f'<div class="hint-placeholder" data-hint-id="{len(hints)-1}"></div>'

            # Заменяем [hint]...[/hint] на плейсхолдеры
            processed_content = re.sub(r'\[hint](.*?)\[/hint]', process_hint, content, flags=re.DOTALL)

            # Конвертируем основной контент (без скрытых фрагментов)
            html_content = markdown2.markdown(processed_content, extras=["tables", "fenced-code-blocks"])

            # Подготовка данных для таймера
            timer_data = {
                'enabled': self.enable_timer.get(),
                'hours': int(self.timer_hours.get()),
                'minutes': int(self.timer_minutes.get()),
                'seconds': int(self.timer_seconds.get()),
                'end_time': None
            }

            if timer_data['enabled']:
                total_seconds = (timer_data['hours'] * 3600 +
                                 timer_data['minutes'] * 60 +
                                 timer_data['seconds'])
                timer_data['end_time'] = (datetime.now() + timedelta(seconds=total_seconds)).isoformat()

            # Подготовка данных для ограничения фрагментов
            limit_data = {
                'enabled': self.enable_limit.get(),
                'max_fragments': int(self.max_fragments.get()) if self.enable_limit.get() else 0
            }

            # Заполняем шаблон
            final_html = self.html_template.replace('{html_content}', html_content)
            final_html = final_html.replace('{hints}', json.dumps(hints))
            final_html = final_html.replace('{hints_count}', str(len(hints)))
            final_html = final_html.replace('{key_hash}', key_hash)
            final_html = final_html.replace('{timer_data}', json.dumps(timer_data))
            final_html = final_html.replace('{limit_data}', json.dumps(limit_data))  # Добавляем данные об ограничении

            # Сохраняем результат
            with open(self.output_file.get(), 'w', encoding='utf-8') as f:
                f.write(final_html)

            messagebox.showinfo(
                "Success",
                f"HTML file created successfully!\n"
                f"Contains {len(hints)} protected fragments.\n"
                f"Timer: {'Enabled' if timer_data['enabled'] else 'Disabled'}"
            )

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


if __name__ == "__main__":
    root = tk.Tk()
    app = MarkdownToProtectedHTMLConverter(root)
    root.mainloop()
