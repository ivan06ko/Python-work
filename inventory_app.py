import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime


class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Облік товарів (CSV, Tkinter)")
        self.root.geometry("950x550")

        self.items = []
        self.current_file = None

        self.sort_column = None
        self.sort_reverse = False

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

    def create_widgets(self):
        top_frame = ttk.Frame(self.root, padding=5)
        top_frame.pack(side=tk.TOP, fill=tk.X)
        ttk.Label(top_frame, text="Пошук (назва/категорія):").pack(side=tk.LEFT)
        ttk.Entry(top_frame, textvariable=self.search_var, width=40).pack(side=tk.LEFT, padx=5)

        main_frame = ttk.Frame(self.root, padding=5)
        main_frame.pack(fill=tk.BOTH, expand=True)

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
        self.tree.column("name", width=140)
        self.tree.column("category", width=110)
        self.tree.column("quantity", width=70, anchor=tk.CENTER)
        self.tree.column("price", width=70, anchor=tk.E)
        self.tree.column("location", width=110)
        self.tree.column("created_at", width=140)

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        form_frame = ttk.Frame(main_frame, padding=10)
        form_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.id_entry = self.create_labeled_entry(form_frame, "ID:", self.id_var)
        self.name_entry = self.create_labeled_entry(form_frame, "Назва:", self.name_var)
        self.category_entry = self.create_labeled_entry(form_frame, "Категорія:", self.category_var)
        self.quantity_entry = self.create_labeled_entry(form_frame, "Кількість:", self.quantity_var)
        self.price_entry = self.create_labeled_entry(form_frame, "Ціна:", self.price_var)
        self.location_entry = self.create_labeled_entry(form_frame, "Розташування:", self.location_var)

        ttk.Label(form_frame, text="Створено:").pack(anchor=tk.W)
        self.created_at_entry = tk.Entry(form_frame, textvariable=self.created_at_var, state="readonly")
        self.created_at_entry.pack(fill=tk.X, pady=(0, 10))

        btn_frame = ttk.Frame(form_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        ttk.Button(btn_frame, text="Додати", command=self.add_item).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="Оновити", command=self.update_item).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="Видалити", command=self.delete_item).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="Очистити форму", command=self.clear_form).pack(fill=tk.X, pady=2)

        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_labeled_entry(self, parent, label_text, text_var):
        ttk.Label(parent, text=label_text).pack(anchor=tk.W)
        entry = tk.Entry(parent, textvariable=text_var)
        entry.pack(fill=tk.X, pady=(0, 5))
        return entry

    def bind_events(self):
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.search_var.trace_add("write", lambda *args: self.apply_filter())

    def refresh_tree(self, items_to_show=None):
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
        for item in self.items:
            if str(item["id"]) == str(item_id):
                return item
        return None

    def apply_filter(self):
        text = self.search_var.get().strip().lower()
        if not text:
            self.refresh_tree()
            self.set_status("Фільтр вимкнено")
            return
        filtered = [
            item
            for item in self.items
            if text in item["name"].lower() or text in item["category"].lower()
        ]
        self.refresh_tree(filtered)
        self.set_status(f"Знайдено записів: {len(filtered)}")

    def sort_by_column(self, column):
        if not self.items:
            return
        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = column
            self.sort_reverse = False

        def sort_key(item):
            value = item.get(column)
            if column in ("quantity", "price"):
                return float(value)
            if column == "created_at":
                try:
                    return datetime.fromisoformat(str(value))
                except Exception:
                    return str(value)
            return str(value).lower()

        self.items.sort(key=sort_key, reverse=self.sort_reverse)
        self.apply_filter()

    def reset_entry_styles(self):
        for e in (
            self.id_entry,
            self.name_entry,
            self.category_entry,
            self.quantity_entry,
            self.price_entry,
            self.location_entry,
        ):
            e.config(bg="white")

    def validate_form(self, allow_existing_id=None):
        self.reset_entry_styles()
        errors = []

        id_val = self.id_var.get().strip()
        name = self.name_var.get().strip()
        category = self.category_var.get().strip()
        quantity_str = self.quantity_var.get().strip()
        price_str = self.price_var.get().strip().replace(",", ".")
        location = self.location_var.get().strip()

        if not name:
            errors.append("Назва не може бути порожньою")
            self.name_entry.config(bg="#ffcccc")
        if not category:
            errors.append("Категорія не може бути порожньою")
            self.category_entry.config(bg="#ffcccc")

        try:
            quantity = int(quantity_str)
            if quantity < 0:
                raise ValueError
        except Exception:
            errors.append("Кількість має бути цілим числом ≥ 0")
            self.quantity_entry.config(bg="#ffcccc")
            quantity = None

        try:
            price = float(price_str)
            if price < 0:
                raise ValueError
        except Exception:
            errors.append("Ціна має бути числом ≥ 0")
            self.price_entry.config(bg="#ffcccc")
            price = None

        existing_ids = {str(item["id"]) for item in self.items}
        if not id_val:
            new_id = 1
            while str(new_id) in existing_ids:
                new_id += 1
            id_val = str(new_id)
        else:
            if id_val in existing_ids and id_val != str(allow_existing_id):
                errors.append(f"ID '{id_val}' вже існує")
                self.id_entry.config(bg="#ffcccc")

        if errors:
            self.set_status("; ".join(errors))
            messagebox.showwarning("Помилка введення", "\n".join(errors))
            return None

        return {
            "id": id_val,
            "name": name,
            "category": category,
            "quantity": quantity,
            "price": price,
            "location": location,
        }

    def add_item(self):
        data = self.validate_form()
        if not data:
            return
        data["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.items.append(data)
        self.apply_filter()
        self.select_item_in_tree(data["id"])
        self.set_status(f"Додано товар ID={data['id']}")

    def update_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Оновлення", "Виберіть запис у таблиці")
            return
        original_id = selected[0]
        item = self.find_item_by_id(original_id)
        if not item:
            messagebox.showerror("Помилка", "Запис не знайдено")
            return
        data = self.validate_form(allow_existing_id=original_id)
        if not data:
            return
        data["created_at"] = item["created_at"]
        item.update(data)
        self.apply_filter()
        self.select_item_in_tree(item["id"])
        self.set_status(f"Оновлено товар ID={item['id']}")

    def delete_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Видалення", "Виберіть запис у таблиці")
            return
        iid = selected[0]
        item = self.find_item_by_id(iid)
        if not item:
            messagebox.showerror("Помилка", "Запис не знайдено")
            return
        if not messagebox.askyesno("Підтвердження", f"Видалити товар ID={item['id']}?"):
            return
        self.items = [i for i in self.items if str(i["id"]) != str(iid)]
        self.apply_filter()
        self.clear_form()
        self.set_status(f"Видалено товар ID={item['id']}")

    def clear_form(self):
        self.id_var.set("")
        self.name_var.set("")
        self.category_var.set("")
        self.quantity_var.set("")
        self.price_var.set("")
        self.location_var.set("")
        self.created_at_var.set("")
        self.reset_entry_styles()
        self.tree.selection_remove(self.tree.selection())
        self.set_status("Форма очищена")

    def select_item_in_tree(self, item_id):
        iid = str(item_id)
        if iid in self.tree.get_children():
            self.tree.selection_set(iid)
            self.tree.see(iid)

    def open_csv(self):
        filename = filedialog.askopenfilename(
            title="Відкрити CSV",
            filetypes=[("CSV файли", "*.csv"), ("Всі файли", "*.*")],
        )
        if not filename:
            return
        try:
            with open(filename, "r", newline="", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                required = [
                    "id",
                    "name",
                    "category",
                    "quantity",
                    "price",
                    "location",
                    "created_at",
                ]
                for field in required:
                    if field not in reader.fieldnames:
                        raise ValueError(f"Немає поля '{field}' у заголовку CSV")
                new_items = []
                for row in reader:
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
            self.items = new_items
            self.current_file = filename
            self.apply_filter()
            self.clear_form()
            self.set_status(
                f"Завантажено {len(self.items)} записів із '{os.path.basename(filename)}'"
            )
        except Exception as e:
            messagebox.showerror("Помилка відкриття CSV", str(e))
            self.set_status(f"Помилка відкриття: {e}")

    def save_csv(self):
        if not self.current_file:
            return self.save_csv_as()
        self._write_csv(self.current_file)

    def save_csv_as(self):
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
                    writer.writerow(
                        {
                            "id": item["id"],
                            "name": item["name"],
                            "category": item["category"],
                            "quantity": int(item["quantity"]),
                            "price": float(item["price"]),
                            "location": item["location"],
                            "created_at": item["created_at"],
                        }
                    )
            self.set_status(
                f"Збережено {len(self.items)} записів у '{os.path.basename(filename)}'"
            )
            messagebox.showinfo("Збережено", "Дані успішно збережені")
        except Exception as e:
            messagebox.showerror("Помилка збереження CSV", str(e))
            self.set_status(f"Помилка збереження: {e}")

    def set_status(self, message):
        self.status_var.set(message)


def main():
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
