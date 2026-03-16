"""
Тесты для калькулятора c обратной польской нотацией (ОПН/RPN)

Этот модуль содержит набор unit-тестов для проверки корректности работы
калькулятора, который преобразует инфиксные выражения в постфиксные (ОПН)
и вычисляет их результат.
"""
import unittest
from main import tokenize, infix_to_rpn, eval_rpn, calculate


class TestTokenize(unittest.TestCase):
    """Тесты функции токенизации"""

    def test_simple_numbers(self):
        """Простые числа"""
        self.assertEqual(tokenize("123"), ["123"])
        self.assertEqual(tokenize("1 2 3"), ["1", "2", "3"])

    def test_decimal_numbers(self):
        """Дробные числа"""
        self.assertEqual(tokenize("3.14"), ["3.14"])
        self.assertEqual(tokenize("2.5 + 3.7"), ["2.5", "+", "3.7"])

    def test_operators(self):
        """Операторы"""
        self.assertEqual(tokenize("1+2"), ["1", "+", "2"])
        self.assertEqual(tokenize("1 * 2"), ["1", "*", "2"])
        self.assertEqual(tokenize("10 / 2"), ["10", "/", "2"])

    def test_all_operators(self):
        """Все поддерживаемые операторы"""
        result = tokenize("1 + 2 - 3 * 4 / 5 % 6 ^ 7")
        expected = ["1", "+", "2", "-", "3", "*", "4", "/", "5", "%", "6", "^", "7"]
        self.assertEqual(result, expected)

    def test_parentheses(self):
        """Скобки"""
        self.assertEqual(tokenize("(1 + 2)"), ["(", "1", "+", "2", ")"])
        self.assertEqual(tokenize("((1 + 2))"), ["(", "(", "1", "+", "2", ")", ")"])

    def test_spaces(self):
        """Пробелы игнорируются"""
        self.assertEqual(tokenize("  1  +  2  "), ["1", "+", "2"])
        self.assertEqual(tokenize(""), [])

    def test_complex_expression(self):
        """Сложное выражение"""
        result = tokenize("2 + 3 * (4 - 1)")
        expected = ["2", "+", "3", "*", "(", "4", "-", "1", ")"]
        self.assertEqual(result, expected)


class TestInfixToRPN(unittest.TestCase):
    """Тесты преобразования в ОПН"""

    def test_single_number(self):
        """Одно число"""
        self.assertEqual(infix_to_rpn(["5"]), ["5"])

    def test_simple_addition(self):
        """Простое сложение"""
        self.assertEqual(infix_to_rpn(["1", "+", "2"]), ["1", "2", "+"])

    def test_simple_subtraction(self):
        """Простое вычитание"""
        self.assertEqual(infix_to_rpn(["5", "-", "3"]), ["5", "3", "-"])

    def test_priority_multiplication(self):
        """Приоритет умножения"""
        # 1 + 2 * 3 → 1 2 3 * +
        self.assertEqual(
            infix_to_rpn(["1", "+", "2", "*", "3"]), ["1", "2", "3", "*", "+"]
        )

    def test_priority_division(self):
        """Приоритет деления"""
        # 10 / 2 + 3 → 10 2 / 3 +
        self.assertEqual(
            infix_to_rpn(["10", "/", "2", "+", "3"]), ["10", "2", "/", "3", "+"]
        )

    def test_priority_power(self):
        """Приоритет степени (уровень 3)"""
        # 2 + 3 ^ 2 → 2 3 2 ^ +
        self.assertEqual(
            infix_to_rpn(["2", "+", "3", "^", "2"]), ["2", "3", "2", "^", "+"]
        )

    def test_parentheses_override(self):
        """Скобки меняют приоритет"""
        # (1 + 2) * 3 → 1 2 + 3 *
        self.assertEqual(
            infix_to_rpn(["(", "1", "+", "2", ")", "*", "3"]), ["1", "2", "+", "3", "*"]
        )

    def test_nested_parentheses(self):
        """Вложенные скобки"""
        # ((1 + 2) * 3) → 1 2 + 3 *
        result = infix_to_rpn(["(", "(", "1", "+", "2", ")", "*", "3", ")"])
        self.assertEqual(result, ["1", "2", "+", "3", "*"])

    def test_complex_expression(self):
        """Сложное выражение из примера"""
        # 2 + 3 * (4 - 1) ^ 2 → 2 3 4 1 - 2 ^ * +
        tokens = ["2", "+", "3", "*", "(", "4", "-", "1", ")", "^", "2"]
        expected = ["2", "3", "4", "1", "-", "2", "^", "*", "+"]
        self.assertEqual(infix_to_rpn(tokens), expected)

    def test_all_priority_levels(self):
        """Все 3 уровня приоритета"""
        # 1 + 2 * 3 ^ 2 → 1 2 3 2 ^ * +
        tokens = ["1", "+", "2", "*", "3", "^", "2"]
        expected = ["1", "2", "3", "2", "^", "*", "+"]
        self.assertEqual(infix_to_rpn(tokens), expected)

    def test_modulo_operator(self):
        """Оператор остатка от деления"""
        # 10 % 3 + 2 → 10 3 % 2 +
        self.assertEqual(
            infix_to_rpn(["10", "%", "3", "+", "2"]), ["10", "3", "%", "2", "+"]
        )


class TestEvalRPN(unittest.TestCase):
    """Тесты вычисления ОПН"""

    def test_single_number(self):
        """Одно число"""
        self.assertEqual(eval_rpn(["5"]), 5.0)

    def test_addition(self):
        """Сложение"""
        self.assertEqual(eval_rpn(["2", "3", "+"]), 5.0)

    def test_subtraction(self):
        """Вычитание"""
        self.assertEqual(eval_rpn(["5", "3", "-"]), 2.0)

    def test_multiplication(self):
        """Умножение"""
        self.assertEqual(eval_rpn(["4", "3", "*"]), 12.0)

    def test_division(self):
        """Деление"""
        self.assertEqual(eval_rpn(["10", "2", "/"]), 5.0)

    def test_power(self):
        """Возведение в степень"""
        self.assertEqual(eval_rpn(["2", "3", "^"]), 8.0)
        self.assertEqual(eval_rpn(["3", "2", "^"]), 9.0)

    def test_modulo(self):
        """Остаток от деления"""
        self.assertEqual(eval_rpn(["10", "3", "%"]), 1.0)

    def test_complex_rpn(self):
        """Сложное ОПН выражение"""
        # 2 3 4 1 - 2 ^ * + = 29
        rpn = ["2", "3", "4", "1", "-", "2", "^", "*", "+"]
        self.assertEqual(eval_rpn(rpn), 29.0)

    def test_decimal_result(self):
        """Дробный результат"""
        self.assertEqual(eval_rpn(["5", "2", "/"]), 2.5)

    def test_negative_result(self):
        """Отрицательный результат"""
        self.assertEqual(eval_rpn(["3", "5", "-"]), -2.0)


class TestCalculate(unittest.TestCase):
    """Тесты полной функции calculate"""

    def test_simple_addition(self):
        """Простое сложение"""
        self.assertEqual(calculate("2 + 3"), 5)

    def test_simple_multiplication(self):
        """Простое умножение"""
        self.assertEqual(calculate("4 * 5"), 20)

    def test_priority_operations(self):
        """Приоритет операций"""
        self.assertEqual(calculate("2 + 3 * 4"), 14)
        self.assertEqual(calculate("10 - 2 * 3"), 4)

    def test_parentheses(self):
        """Скобки"""
        self.assertEqual(calculate("(2 + 3) * 4"), 20)
        self.assertEqual(calculate("2 + (3 * 4)"), 14)

    def test_three_priority_levels(self):
        """Все 3 уровня приоритета"""
        # ^ (3) > * (2) > + (1)
        self.assertEqual(calculate("2 + 3 * 4 ^ 2"), 50)  # 2 + 3 * 16 = 50

    def test_complex_expression(self):
        """Сложное выражение"""
        self.assertEqual(calculate("2 + 3 * (4 - 1) ^ 2"), 29)

    def test_division(self):
        """Деление"""
        self.assertEqual(calculate("10 / 2"), 5)
        self.assertEqual(calculate("7 / 2"), 3.5)

    def test_modulo(self):
        """Остаток от деления"""
        self.assertEqual(calculate("10 % 3"), 1)

    def test_power(self):
        """Степень"""
        self.assertEqual(calculate("2 ^ 3"), 8)
        self.assertEqual(calculate("2 ^ 10"), 1024)

    def test_nested_parentheses(self):
        """Вложенные скобки"""
        self.assertEqual(calculate("((2 + 3) * 4)"), 20)
        self.assertEqual(calculate("(1 + 2) * (3 + 4)"), 21)

    def test_spaces_handling(self):
        """Обработка пробелов"""
        self.assertEqual(calculate("  2  +  3  "), 5)
        self.assertEqual(calculate("2+3"), 5)

    def test_decimal_numbers(self):
        """Дробные числа"""
        result = calculate("2.5 + 3.5")
        self.assertEqual(result, 6)


class TestEdgeCases(unittest.TestCase):
    """Тесты граничных случаев"""

    def test_zero_operations(self):
        """Операции c нулём"""
        self.assertEqual(calculate("0 + 5"), 5)
        self.assertEqual(calculate("5 * 0"), 0)
        self.assertEqual(calculate("0 ^ 5"), 0)

    def test_large_numbers(self):
        """Большие числа"""
        self.assertEqual(calculate("1000 + 2000"), 3000)
        self.assertEqual(calculate("100 * 100"), 10000)

    def test_consecutive_operations(self):
        """Последовательные операции одного приоритета"""
        self.assertEqual(calculate("1 + 2 + 3"), 6)
        self.assertEqual(calculate("10 - 5 - 2"), 3)
        self.assertEqual(calculate("2 * 3 * 4"), 24)

    def test_mixed_operations(self):
        """Смешанные операции"""
        self.assertEqual(calculate("10 + 5 * 2 - 3"), 17)
        self.assertEqual(calculate("100 / 10 + 5 * 2"), 20)


# ==================== ЗАПУСК ТЕСТОВ ====================

if __name__ == "__main__":
    # Запуск всех тестов
    unittest.main(verbosity=2)

    # Примеры использования калькулятора
    print("\n" + "=" * 50)
    print("Examples")
    print("=" * 50)

    test_cases = [
        "2 + 3",
        "2 + 3 * 4",
        "(2 + 3) * 4",
        "2 + 3 * (4 - 1) ^ 2",
        "10 / 2 + 3",
        "2 ^ 3 ^ 2",
        "10 % 3",
        "((1 + 2) * 3) + 4",
    ]

    for expr in test_cases:
        print(f"\n{expr} = {calculate(expr)}")
