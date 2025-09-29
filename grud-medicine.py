meds = [
    {"назва": "Амоксицилін", "кількість": 120, "категорія": "antibiotic", "температура": 8.0},
    {"назва": "Вітамін C", "кількість": "50", "категорія": "vitamin", "температура": 22.5},
    {"назва": "COVID-Vac", "кількість": 300, "категорія": "vaccine", "температура": -2.0},
    {"назва": "Ноотроп", "кількість": 200, "категорія": "nootrop", "температура": 18.0}
]

for m in meds:
    if not isinstance(m["кількість"], int) or not isinstance(m["температура"], (int, float)):
        print(f"{m['назва']}: Помилка даних")
        continue
#prototype of medicine storage system 

if m["температура"] < 5: temp = "надто холодно"
elif m["температура"] > 25: temp = "надто жарко"
else:temp = "температура в нормі"

match m["категорія"]:
    case "antibiotic": cat = "рецептурний препаратик"
    case "vitamin": cat = "Вільний продаж"
    case "vaccine": cat = "потребує бути в спеціальних умовах прожиття"
    case _: cat = "Решта"

print(f"{m['назва']}: {cat}, {temp}")

#prolly last prototype before release