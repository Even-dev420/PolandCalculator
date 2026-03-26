"""
Калькулятор c обратной польской нотацией
"""
priority = {"+": 1, "-": 1, "*": 2, "/": 2, "%": 2, "^": 3}

def tokenize(expr):
    """Разбивает строку на числа и операторы"""
    tokens = []
    i = 0
    while i < len(expr):
        if expr[i].isspace():
            i += 1
        elif expr[i].isdigit() or expr[i] == ".":
            num = ""
            while i < len(expr) and (expr[i].isdigit() or expr[i] == "."):
                num += expr[i]
                i += 1
            tokens.append(num)
        elif expr[i] in "+-*/%^()":
            tokens.append(expr[i])
            i += 1
        else:
            i += 1
    return tokens


def infix_to_rpn(tokens):
    """Преобразует инфиксную запись в ОПН"""
    output = []
    stack = []


    for token in tokens:
        if token.replace(".", "").isdigit():  # Если число
            output.append(token)
        elif token == "(":
            stack.append(token)
        elif token == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            stack.pop()  # Удаляем '('
        else:  # Если оператор
            while (
                stack
                and stack[-1] != "("
                and (
                    priority.get(stack[-1], 0) > priority.get(token, 0)
                    or (
                        priority.get(stack[-1], 0) == priority.get(token, 0)
                        and token != "^"  # ^ — правоассоциативный, остальные — лево
                    )
                )
            ):
                output.append(stack.pop())
            stack.append(token)

    while stack:
        output.append(stack.pop())

    return output


def eval_rpn(rpn):
    """Вычисляет выражение в ОПН"""
    stack = []

    for token in rpn:
        if token.replace(".", "").isdigit():
            stack.append(float(token))
        else:
            b = stack.pop()
            a = stack.pop()

            if token == "+":
                stack.append(a + b)
            elif token == "-":
                stack.append(a - b)
            elif token == "*":
                stack.append(a * b)
            elif token == "/":
                stack.append(a / b)
            elif token == "%":
                stack.append(a % b)
            elif token == "^":
                stack.append(a**b)

    return stack[0]


def calculate(expr):
    """Посчитать выражение"""
    print(f"\nExpression: {expr}")

    tokens = tokenize(expr)
    print(f"Tokens: {tokens}")

    rpn = infix_to_rpn(tokens)
    print(f"REVPOL: {' '.join(rpn)}")

    result = eval_rpn(rpn)
    print(f"Result: {result}")

    if result == int(result):
        return int(result)
    return result


# Примеры использования
if __name__ == "__main__":
    print("=== Poland Calculator")

    # Тестовые примеры
    test_exprs = [
        "2 + 3 * 4",
        "2 + 3 * (4 - 1) ^ 2",
        "( 10 + 5 ) / 3"
    ]

    for test_expr in test_exprs:
        calculate(test_expr)
