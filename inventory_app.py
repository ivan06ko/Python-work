import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime


class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Облік товарів (CSV, Tkinter)")
        self.root.geometry("1000x600")

        # Список товарів у пам'яті
        self.items = []  # кожен елемент: dict з полями товару
        self.current_file = None  # шлях до відкритого CSV

        # Для сортування таблиці
        self.sort_column = None
        self.sort_reverse = False

        # Створення змінних для полів форми
        self.id_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.quantity_var = tk.StringVar()
        self.price_var = tk.StringVar()
        self.location_var = tk.StringVar()
        self.created_at_var = tk.StringVar()

        self.search_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Готово")

        self.create_menu()
        self.create_widgets()
        self.bind_events()

    # ---------- Створення меню ----------

    def create_menu(self):
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Відкрити CSV...", command=self.open_csv)
        file_menu.add_command(label="Зберегти", command=self.save_csv)
        file_menu.add_command(label="Зберегти як...", command=self.save_csv_as)
        file_menu.add_separator()
        file_menu.add_command(label="Вихід", command=self.root.quit)

        menubar.add_cascade(label="Файл", menu=file_menu)
        self.root.config(menu=menubar)

    # ---------- Основні віджети ----------

    def create_widgets(self):
        # Верхня рамка: пошук
        top_frame = ttk.Frame(self.root, padding=5)
        top_frame.pack(side=tk.TOP, fill=tk.X)

        ttk.Label(top_frame, text="Пошук (назва/категорія):").pack(side=tk.LEFT)
        search_entry = ttk.Entry(top_frame, textvariable=self.search_var, width=40)
        search_entry.pack(side=tk.LEFT, padx=5)

        # Центральна рамка: таблиця + форма
        main_frame = ttk.Frame(self.root, padding=5)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Таблиця (Treeview)
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        columns = ("id", "name", "category", "quantity", "price", "location", "created_at")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        self.tree.heading("id", text="ID", command=lambda: self.sort_by_column("id"))
        self.tree.heading("name", text="Назва", command=lambda: self.sort_by_column("name"))
        self.tree.heading("category", text="Категорія", command=lambda: self.sort_by_column("category"))
        self.tree.heading("quantity", text="Кількість", command=lambda: self.sort_by_column("quantity"))
        self.tree.heading("price", text="Ціна", command=lambda: self.sort_by_column("price"))
        self.tree.heading("location", text="Розташування", command=lambda: self.sort_by_column("location"))
        self.tree.heading("created_at", text="Створено", command=lambda: self.sort_by_column("created_at"))

        self.tree.column("id", width=60, anchor=tk.CENTER)
        self.tree.column("name", width=150)
        self.tree.column("category", width=120)
        self.tree.column("quantity", width=80, anchor=tk.CENTER)
        self.tree.column("price", width=80, anchor=tk.E)
        self.tree.column("location", width=120)
        self.tree.column("created_at", width=150)

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        # Форма праворуч
        form_frame = ttk.Frame(main_frame, padding=10)
        form_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Поля форми (прості tk.Entry, щоб легко міняти фон при помилці)
        self.id_entry = self.create_labeled_entry(form_frame, "ID:", self.id_var)
        self.name_entry = self.create_labeled_entry(form_frame, "Назва:", self.name_var)
        self.category_entry = self.create_labeled_entry(form_frame, "Категорія:", self.category_var)
        self.quantity_entry = self.create_labeled_entry(form_frame, "Кількість:", self.quantity_var)
        self.price_entry = self.create_labeled_entry(form_frame, "Ціна:", self.price_var)
        self.location_entry = self.create_labeled_entry(form_frame, "Розташування:", self.location_var)

        # created_at лише для перегляду
        ttk.Label(form_frame, text="Створено:").pack(anchor=tk.W)
        self.created_at_entry = tk.Entry(form_frame, textvariable=self.created_at_var, state="readonly")
        self.created_at_entry.pack(fill=tk.X, pady=(0, 10))

        # Кнопки CRUD
        btn_frame = ttk.Frame(form_frame)
        btn_frame.pack(fill=tk.X, pady=5)

        self.add_btn = ttk.Button(btn_frame, text="Додати", command=self.add_item)
        self.update_btn = ttk.Button(btn_frame, text="Оновити", command=self.update_item)
        self.delete_btn = ttk.Button(btn_frame, text="Видалити", command=self.delete_item)
        self.clear_btn = ttk.Button(btn_frame, text="Очистити форму", command=self.clear_form)

        self.add_btn.pack(fill=tk.X, pady=2)
        self.update_btn.pack(fill=tk.X, pady=2)
        self.delete_btn.pack(fill=tk.X, pady=2)
        self.clear_btn.pack(fill=tk.X, pady=2)

        # Status bar
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_labeled_entry(self, parent, label_text, text_var):
        """Допоміжний метод: підпис + поле вводу."""
        ttk.Label(parent, text=label_text).pack(anchor=tk.W)
        entry = tk.Entry(parent, textvariable=text_var)
        entry.pack(fill=tk.X, pady=(0, 5))
        return entry

    # ---------- Події ----------

    def bind_events(self):
        # Селект рядка в таблиці
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Пошук
        self.search_var.trace_add("write", lambda *args: self.apply_filter())

    # ---------- Робота з таблицею ----------

    def refresh_tree(self, items_to_show=None):
        """Перемалювати таблицю згідно з переданим списком (або всіх)."""
        if items_to_show is None:
            items_to_show = self.items

        self.tree.delete(*self.tree.get_children())
        for item in items_to_show:
            self.tree.insert(
                "",
                tk.END,
                iid=str(item["id"]),
                values=(
                    item["id"],
                    item["name"],
                    item["category"],
                    item["quantity"],
                    f"{item['price']:.2f}",
                    item["location"],
                    item["created_at"],
                ),
            )

    def on_tree_select(self, event):
        """Заповнити форму даними вибраного рядка."""
        selected = self.tree.selection()
        if not selected:
            return

        iid = selected[0]
        item = self.find_item_by_id(iid)
        if not item:
            return

        self.reset_entry_styles()

        self.id_var.set(item["id"])
        self.name_var.set(item["name"])
        self.category_var.set(item["category"])
        self.quantity_var.set(str(item["quantity"]))
        self.price_var.set(str(item["price"]))
        self.location_var.set(item["location"])
        self.created_at_var.set(item["created_at"])
        self.set_status(f"Вибрано товар ID={item['id']}")

    def find_item_by_id(self, item_id):
        """Пошук товару в пам'яті за ID."""
        for item in self.items:
            if str(item["id"]) == str(item_id):
                return item
        return None

    # ---------- Пошук і фільтрація ----------

    def apply_filter(self):
        """Фільтрувати список за полем пошуку."""
        text = self.search_var.get().strip().lower()
        if not text:
            self.refresh_tree()
            self.set_status("Фільтр вимкнено")
            return

        filtered = []
        for item in self.items:
            if text in item["name"].lower() or text in item["category"].lower():
                filtered.append(item)

        self.refresh_tree(filtered)
        self.set_status(f"Знайдено записів: {len(filtered)}")

    def sort_by_column(self, column):
        """Сортування списку товарів за колонкою."""
        if not self.items:
            return

        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = column
            self.sort_reverse = False

        def sort_key(item):
            value = item.get(column)
            # Спроба числового сортування для quantity та price
            if column in ("quantity", "price"):
                return float(value)
            # Для created_at сорт по даті, якщо формат дозволяє
            if column == "created_at":
                try:
                    return datetime.fromisoformat(str(value))
                except Exception:
                    return str(value)
            return str(value).lower()

        self.items.sort(key=sort_key, reverse=self.sort_reverse)
        self.apply_filter()  # з урахуванням поточного фільтра

        direction = "за спаданням" if self.sort_reverse else "за зростанням"
        self.set_status(f"Відсортовано за '{column}' ({direction})")

    # ---------- Валідація форми ----------

    def reset_entry_styles(self):
        """Скинути підсвічування помилок."""
        normal_bg = "white"
        for e in (
            self.id_entry,
            self.name_entry,
            self.category_entry,
            self.quantity_entry,
            self.price_entry,
            self.location_entry,
        ):
            e.config(bg=normal_bg)

    def validate_form(self, allow_existing_id=None):
        """
        Перевірка полів форми.
        allow_existing_id — ID, який дозволено повторити (для оновлення).
        Повертає dict з даними або None, якщо є помилки.
        """
        self.reset_entry_styles()
        errors = []

        id_val = self.id_var.get().strip()
        name = self.name_var.get().strip()
        category = self.category_var.get().strip()
        quantity_str = self.quantity_var.get().strip()
        price_str = self.price_var.get().strip().replace(",", ".")
        location = self.location_var.get().strip()

        # name, category
        if not name:
            errors.append("Назва не може бути порожньою")
            self.name_entry.config(bg="#ffcccc")
        if not category:
            errors.append("Категорія не може бути порожньою")
            self.category_entry.config(bg="#ffcccc")

        # quantity
        try:
            quantity = int(quantity_str)
            if quantity < 0:
                raise ValueError
        except Exception:
            errors.append("Кількість має бути цілим числом ≥ 0")
            self.quantity_entry.config(bg="#ffcccc")
            quantity = None

        # price
        try:
            price = float(price_str)
            if price < 0:
                raise ValueError
        except Exception:
            errors.append("Ціна має бути числом ≥ 0")
            self.price_entry.config(bg="#ffcccc")
            price = None

        # ID: якщо порожній — згенерувати
        existing_ids = {str(item["id"]) for item in self.items}
        if not id_val:
            new_id = 1
            while str(new_id) in existing_ids:
                new_id += 1
            id_val = str(new_id)
        else:
            # Перевірка унікальності
            if id_val in existing_ids and id_val != str(allow_existing_id):
                errors.append(f"ID '{id_val}' вже існує, вкажіть інший")
                self.id_entry.config(bg="#ffcccc")

        if errors:
            self.set_status("; ".join(errors))
            messagebox.showwarning("Помилка введення", "\n".join(errors))
            return None

        data = {
            "id": id_val,
            "name": name,
            "category": category,
            "quantity": quantity,
            "price": price,
            "location": location,
        }

        return data

    # ---------- CRUD операції ----------

    def add_item(self):
        """Додати новий товар."""
        data = self.validate_form()
        if not data:
            return

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data["created_at"] = now_str

        self.items.append(data)
        self.apply_filter()
        self.select_item_in_tree(data["id"])
        self.set_status(f"Додано товар ID={data['id']}")

    def update_item(self):
        """Оновити вибраний товар."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Оновлення", "Спочатку виберіть запис у таблиці")
            self.set_status("Немає вибраного запису для оновлення")
            return

        original_id = selected[0]
        item = self.find_item_by_id(original_id)
        if not item:
            messagebox.showerror("Помилка", "Не вдалося знайти запис у пам'яті")
            return

        data = self.validate_form(allow_existing_id=original_id)
        if not data:
            return

        # Зберегти created_at старий
        data["created_at"] = item["created_at"]

        # Оновити dict
        item.update(data)

        self.apply_filter()
        self.select_item_in_tree(item["id"])
        self.set_status(f"Оновлено товар ID={item['id']}")

    def delete_item(self):
        """Видалити вибраний товар (з підтвердженням)."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Видалення", "Спочатку виберіть запис у таблиці")
            self.set_status("Немає вибраного запису для видалення")
            return

        iid = selected[0]
        item = self.find_item_by_id(iid)
        if not item:
            messagebox.showerror("Помилка", "Не вдалося знайти запис у пам'яті")
            return

        if not messagebox.askyesno(
            "Підтвердження видалення",
            f"Видалити товар ID={item['id']} ('{item['name']}')?",
        ):
            return

        self.items = [i for i in self.items if str(i["id"]) != str(iid)]
        self.apply_filter()
        self.clear_form()
        self.set_status(f"Видалено товар ID={item['id']}")

    def clear_form(self):
        """Очистити всі поля форми."""
        self.id_var.set("")
        self.name_var.set("")
        self.category_var.set("")
        self.quantity_var.set("")
        self.price_var.set("")
        self.location_var.set("")
        self.created_at_var.set("")
        self.reset_entry_styles()
        self.tree.selection_remove(self.tree.selection())
        self.set_status("Форму очищено")

    def select_item_in_tree(self, item_id):
        """Виділити рядок у таблиці за ID."""
        iid = str(item_id)
        if iid in self.tree.get_children():
            self.tree.selection_set(iid)
            self.tree.see(iid)

    # ---------- Робота з CSV ----------

    def open_csv(self):
        """Завантажити дані з CSV (повна заміна поточних)."""
        filename = filedialog.askopenfilename(
            title="Відкрити CSV",
            filetypes=[("CSV файли", "*.csv"), ("Всі файли", "*.*")],
        )
        if not filename:
            return

        try:
            with open(filename, "r", newline="", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                required_fields = [
                    "id",
                    "name",
                    "category",
                    "quantity",
                    "price",
                    "location",
                    "created_at",
                ]
                for field in required_fields:
                    if field not in reader.fieldnames:
                        raise ValueError(
                            f"У файлі відсутнє обов'язкове поле '{field}'"
                        )

                new_items = []
                for row in reader:
                    try:
                        item = {
                            "id": str(row["id"]).strip(),
                            "name": str(row["name"]).strip(),
                            "category": str(row["category"]).strip(),
                            "quantity": int(row["quantity"]),
                            "price": float(str(row["price"]).replace(",", ".")),
                            "location": str(row["location"]).strip(),
                            "created_at": str(row["created_at"]).strip(),
                        }
                        new_items.append(item)
                    except Exception as e:
                        raise ValueError(
                            f"Помилка у рядку CSV: {row}\nДеталі: {e}"
                        )

            self.items = new_items
            self.current_file = filename
            self.apply_filter()
            self.clear_form()
            self.set_status(f"Завантажено {len(self.items)} записів із '{os.path.basename(filename)}'")
        except Exception as e:
            messagebox.showerror("Помилка відкриття CSV", str(e))
            self.set_status(f"Помилка відкриття: {e}")

    def save_csv(self):
        """Зберегти у поточний файл, або запитати 'Зберегти як'."""
        if not self.current_file:
            return self.save_csv_as()

        self._write_csv(self.current_file)

    def save_csv_as(self):
        """Зберегти у новий CSV-файл."""
        filename = filedialog.asksavefilename(
            title="Зберегти CSV як...",
            defaultextension=".csv",
            filetypes=[("CSV файли", "*.csv"), ("Всі файли", "*.*")],
        )
        if not filename:
            return

        self._write_csv(filename)
        self.current_file = filename

    def _write_csv(self, filename):
        """Внутрішній метод: записати всі поточні записи у CSV."""
        try:
            with open(filename, "w", newline="", encoding="utf-8-sig") as f:
                fieldnames = [
                    "id",
                    "name",
                    "category",
                    "quantity",
                    "price",
                    "location",
                    "created_at",
                ]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for item in self.items:
                    # Переконатися, що типи серіалізуються нормально
                    row = {
                        "id": item["id"],
                        "name": item["name"],
                        "category": item["category"],
                        "quantity": int(item["quantity"]),
                        "price": float(item["price"]),
                        "location": item["location"],
                        "created_at": item["created_at"],
                    }
                    writer.writerow(row)

            self.set_status(
                f"Дані збережено у '{os.path.basename(filename)}' ({len(self.items)} записів)"
            )
            messagebox.showinfo("Збережено", "Дані успішно збережені")
        except Exception as e:
            messagebox.showerror("Помилка збереження CSV", str(e))
            self.set_status(f"Помилка збереження: {e}")

    # ---------- Службові методи ----------

    def set_status(self, message):
        """Оновити рядок стану."""
        self.status_var.set(message)


def main():
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
