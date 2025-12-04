from dataclasses import dataclass, field
from datetime import datetime
import csv


@dataclass(order=True)
class Item:
    category: str
    value: float
    name: str
    quantity: int
    condition: str
    location: str
    date_added: datetime = field(default_factory=datetime.now, compare=False)

    def total_value(self) -> float:
        return self.quantity * self.value

    def __str__(self) -> str:
        return (
            f"[{self.category}] {self.name} "
            f"({self.quantity} шт.) — {self.value} грн/шт, стан: {self.condition}"
        )


@dataclass
class Inventory:
    items: list[Item] = field(default_factory=list)

    def add_item(self, item: Item) -> None:
        self.items.append(item)

    def remove_item(self, name: str) -> int:
        before = len(self.items)
        self.items = [i for i in self.items if i.name != name]
        return before - len(self.items)

    def find_by_category(self, category: str) -> list[Item]:
        c = category.lower()
        return [i for i in self.items if i.category.lower() == c]

    def total_inventory_value(self) -> float:
        return sum(i.total_value() for i in self.items)

    def save_to_csv(self, filename: str) -> None:
        fields = ["name", "category", "quantity", "value", "condition", "location", "date_added"]
        with open(filename, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            for i in self.items:
                w.writerow({
                    "name": i.name,
                    "category": i.category,
                    "quantity": i.quantity,
                    "value": i.value,
                    "condition": i.condition,
                    "location": i.location,
                    "date_added": i.date_added.isoformat(),
                })

    def load_from_csv(self, filename: str, replace: bool = True) -> None:
        new: list[Item] = []
        with open(filename, "r", newline="", encoding="utf-8") as f:
            r = csv.DictReader(f)
            for row in r:
                item = Item(
                    category=row["category"],
                    value=float(row["value"]),
                    name=row["name"],
                    quantity=int(row["quantity"]),
                    condition=row["condition"],
                    location=row["location"],
                )
                if row.get("date_added"):
                    try:
                        item.date_added = datetime.fromisoformat(row["date_added"])
                    except ValueError:
                        pass
                new.append(item)
        if replace:
            self.items = new
        else:
            self.items.extend(new)

    def export_summary(self) -> str:
        counts: dict[str, int] = {}
        for i in self.items:
            counts[i.category] = counts.get(i.category, 0) + i.quantity
        lines = ["Зведення по категоріях:"]
        for cat in sorted(counts):
            lines.append(f"  - {cat}: {counts[cat]} шт.")
        return "\n".join(lines)

    def filter_items(self, **criteria):
        res = self.items
        for k, v in criteria.items():
            res = [i for i in res if getattr(i, k, None) == v]
        return res

    def sort_items(self, key: str | None = None, reverse: bool = False) -> list[Item]:
        if key is None:
            return sorted(self.items, reverse=reverse)   # за category, потім value
        return sorted(self.items, key=lambda i: getattr(i, key), reverse=reverse)


# --- Невеликий демо-блок, щоб БУЛА відповідь при запуску файлу ---

if __name__ == "__main__":
    inv = Inventory()

    # Додаємо кілька тестових предметів
    inv.add_item(Item(
        category="інструменти",
        value=15.0,
        name="Гаечний ключ",
        quantity=3,
        condition="уживаний",
        location="гараж"
    ))
    inv.add_item(Item(
        category="електроніка",
        value=500.0,
        name="Старий телефон",
        quantity=1,
        condition="зламаний",
        location="комора"
    ))
    inv.add_item(Item(
        category="металобрухт",
        value=10.0,
        name="Залізні труби",
        quantity=7,
        condition="уживаний",
        location="сарай"
    ))

    print("=== Увесь інвентар (відсортований) ===")
    for item in inv.sort_items():
        print(item)

    print("\nЗагальна вартість:", inv.total_inventory_value(), "грн")

    print("\n=== Звіт по категоріях ===")
    print(inv.export_summary())
