num1 = float(input("Вставте перше число: "))
operation = input("Вставте операцію (+, -, *, /): ")
num2 = float(input("Вставте друге число: "))

if operation == "+":
    result = num1 + num2
elif operation == "-":
    result = num1 - num2
elif operation == "*":
    result = num1 * num2
elif operation == "/":
    if num2 != 0:
        result = num1 / num2
    else:
        result = "Помилка: ділення на нуль!"
else:
    result = "Помилка: невідома операція!"

# Вивід результату
print("Результат:", result)