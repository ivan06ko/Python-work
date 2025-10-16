def calc(expr):  # calc приймає рядок expr.
    tokens = list(expr.replace(" ", "")) 
    def helper():
        stack = []
        num = ""
        while tokens:
            t = tokens.pop(0)
            if t.isdigit() or t == '.': #Збирає числа в одне число.
                num += t
            else:
                if num:
                    stack.append(float(num))
                    num = ""
                if t in "+-*/":
                    while len(stack) >= 3 and stack[-2] in "*/" and t in "+-":
                        b, op, a = stack.pop(), stack.pop(), stack.pop()
                        stack.append(a*b if op == '*' else a/b)
                    stack.append(t)
                elif t == '(':
                    stack.append(helper())
                elif t == ')':
                    break
        if num:
            stack.append(float(num))
        while len(stack) >= 3:
            a, op, b = stack.pop(0), stack.pop(0), stack.pop(0)
            stack.insert(0, a+b if op == '+' else a-b if op == '-' else a*b if op == '*' else a/b)
        return stack[0]
    return helper()

# ПУСК
print("Результат:", calc(input("Введіть вираз: ")))