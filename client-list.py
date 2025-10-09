# Clients from the anywhere of the different dimenisions

clients = [
    {"ім'я": "Сетлер", "сума угоди": 50, "статус перевірки": "clean"},
    {"ім'я": "Привид 3ої дивізії", "сума угоди": 700, "статус перевірки": "suspicious"},
    {"ім'я": "Олег", "сума угоди": 1500, "статус перевірки": "fraud"},
    {"ім'я": "Рамштайн", "сума угоди": "сто", "статус перевірки": "unknown"},
    {"ім'я": "Іван", "сума угоди": 350, "статус перевірки": "suspicious"},
]

result = []

for client in clients:
    name = client["ім'я"]
    amount = client["сума угоди"]
    status = client["статус перевірки"]

    # Checkmate
    if not isinstance(amount, (int, float)):
        category = "Фальшифка"
    else:
        # Clasification by amount
        if amount < 100:
            category = "Дрібно"
        elif amount < 1000:
            category = "Середнє"
        else:
            category = "Big Boss"

    # Status
    match status:
        case "clean":
            decision = "Працювати без питань"
        case "suspicious":
            decision = "Перевірити документи"
        case "fraud":
            decision = "У чорний список"
        case _:
            decision = "Невідомий статус"

    result.append(f"{name} → {category}, {decision}")

# result
for r in result:
    print(r)