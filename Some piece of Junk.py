from typing import List

class JunkItem:
    def __init__(self, name: str, quantity: int, value: float):
        self.name = name.strip()
        self.quantity = int(quantity)
        self.value = float(value)

    def __eq__(self, other):
        return (
            isinstance(other, JunkItem)
            and self.name == other.name
            and self.quantity == other.quantity
            and abs(self.value - other.value) < 1e-9 #порівнюэ два числа з плаваючою комою,або щоб не було потипу 0.3000000004 і 0.3
        )

    def __repr__(self):
        return f"{self.name} (x{self.quantity}, {self.value} грн)"

class JunkStorage:
    SEP = '|'

    @staticmethod
    def _encode(x: float) -> str:
        return f"{x}".replace('.', ',')

    @staticmethod
    def _decode(s: str) -> float:
        return float(s.replace(',', '.'))

    @staticmethod
    def serialize(items: List[JunkItem], filename: str):
        with open(filename, 'w', encoding='utf-8') as f:
            for item in items:
                line = f"{item.name}{JunkStorage.SEP}{item.quantity}{JunkStorage.SEP}{JunkStorage._encode(item.value)}\n"
                f.write(line)
        print(f"[ок] Записано {len(items)} рядків у файл '{filename}'")

    @staticmethod
    def parse(filename: str) -> List[JunkItem]:
        items = []
        print(f"[INFO] Зчитую '{filename}'...")
        with open(filename, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                parts = [p.strip() for p in line.strip().split(JunkStorage.SEP)]
                if len(parts) != 3:
                    print(f"Цей  Рядок {i}: неправельний формат, пропускаю")
                    continue
                name, qty, val = parts
                try:
                    items.append(JunkItem(name, int(qty), JunkStorage._decode(val)))
                except Exception:
                    print(f"Цей Рядок {i}: дані напартачені, пропускаю")
        print(f"[ок] Успішно зчитано {len(items)} предметів.\n")
        return items


if __name__ == "__main__":
    stuff = [
        JunkItem("Консервна банка з-під піци", 7, 3.1),
        JunkItem("Пластикові кришки з під курева", 15, 0.9),
        JunkItem("Купка старих проводів Бамбл-бі", 10, 1.2),
        JunkItem("Залізна пластина", 4, 5.6),
    ]

    file_name = "pieces_of_a_damn_junk.txt"

    JunkStorage.serialize(stuff, file_name)

    with open(file_name, 'a', encoding='utf-8') as f:
        f.write("зіпсований рядок\nконсерви|abc|2,5\n")

    loaded = JunkStorage.parse(file_name)

    print(" Знайдено на складі:")
    for item in loaded:
        print(" -", item)
