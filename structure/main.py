from models import Medicine, Antibiotic, Vitamin, Vaccine

def print_infos(items: list[Medicine]) -> None:
    for m in items:
        print(m.info())

def main() -> None:
    items: list[Medicine] = [
        Antibiotic(name="Амоксицилін", quantity=12, price=24.5),
        Vitamin(name="Вітамін C", quantity=20, price=5.0),
        Vaccine(name="Грипол", quantity=5, price=200.0),
        Vaccine(name="Коронавак", quantity=2, price=350.0),
        Antibiotic(name="Азитроміцин", quantity=6, price=31.0),
    ]
    print_infos(items)

if __name__ == "__main__":
    main()