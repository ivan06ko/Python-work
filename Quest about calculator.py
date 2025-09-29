num1 = float(input("Ваше перше число: "))
operation = input("Впишіть операцію (+, -, *, /): ")
num2 = float(input("Ваше друге число: "))

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
        result = "Помилка: ділити на нуль не можна"
else:
    result = "Помилка"

# результат
print("Результат:", result)

#1000 - 1000 = 8?! stupid calculator! 