"""
Тесты для калькулятора c обратной польской нотацией (ОПН/RPN)
"""
import unittest
from main import tokenize, infix_to_rpn, eval_rpn, calculate


class TestTokenize(unittest.TestCase):
    """Tokenization function tests"""

    def test_simple_numbers(self):
        """Prime numbers"""
        self.assertEqual(tokenize("123"), ["123"])
        self.assertEqual(tokenize("1 2 3"), ["1", "2", "3"])

    def test_decimal_numbers(self):
        """Float numbers"""
        self.assertEqual(tokenize("3.14"), ["3.14"])
        self.assertEqual(tokenize("2.5 + 3.7"), ["2.5", "+", "3.7"])

    def test_operators(self):
        """Operators"""
        self.assertEqual(tokenize("1+2"), ["1", "+", "2"])
        self.assertEqual(tokenize("1 * 2"), ["1", "*", "2"])
        self.assertEqual(tokenize("10 / 2"), ["10", "/", "2"])

    def test_all_operators(self):
        """All supported operators"""
        result = tokenize("1 + 2 - 3 * 4 / 5 % 6 ^ 7")
        expected = ["1", "+", "2", "-", "3", "*", "4", "/", "5", "%", "6", "^", "7"]
        self.assertEqual(result, expected)

    def test_brackets(self):
        """Brackets"""
        self.assertEqual(tokenize("(1 + 2)"), ["(", "1", "+", "2", ")"])
        self.assertEqual(tokenize("((1 + 2))"), ["(", "(", "1", "+", "2", ")", ")"])

    def test_spaces(self):
        """Spaces are ignored"""
        self.assertEqual(tokenize("  1  +  2  "), ["1", "+", "2"])
        self.assertEqual(tokenize(""), [])

    def test_complex_expression(self):
        """Complex expression"""
        result = tokenize("2 + 3 * (4 - 1)")
        expected = ["2", "+", "3", "*", "(", "4", "-", "1", ")"]
        self.assertEqual(result, expected)


class TestInfixToRPN(unittest.TestCase):
    """Conversion tests in OPN"""

    def test_single_number(self):
        """One digit"""
        self.assertEqual(infix_to_rpn(["5"]), ["5"])

    def test_simple_addition(self):
        """Simple addition"""
        self.assertEqual(infix_to_rpn(["1", "+", "2"]), ["1", "2", "+"])

    def test_simple_subtraction(self):
        """Simple subtraction"""
        self.assertEqual(infix_to_rpn(["5", "-", "3"]), ["5", "3", "-"])

    def test_priority_multiplication(self):
        """Priority multiplication"""
        # 1 + 2 * 3 → 1 2 3 * +
        self.assertEqual(
            infix_to_rpn(["1", "+", "2", "*", "3"]), ["1", "2", "3", "*", "+"]
        )

    def test_priority_division(self):
        """Priority division"""
        # 10 / 2 + 3 → 10 2 / 3 +
        self.assertEqual(
            infix_to_rpn(["10", "/", "2", "+", "3"]), ["10", "2", "/", "3", "+"]
        )

    def test_priority_power(self):
        """Priority power (level 3)"""
        # 2 + 3 ^ 2 → 2 3 2 ^ +
        self.assertEqual(
            infix_to_rpn(["2", "+", "3", "^", "2"]), ["2", "3", "2", "^", "+"]
        )

    def test_brackets_override(self):
        """Brackets override"""
        # (1 + 2) * 3 → 1 2 + 3 *
        self.assertEqual(
            infix_to_rpn(["(", "1", "+", "2", ")", "*", "3"]), ["1", "2", "+", "3", "*"]
        )

    def test_nested_brackets(self):
        """Nested brackets"""
        # ((1 + 2) * 3) → 1 2 + 3 *
        result = infix_to_rpn(["(", "(", "1", "+", "2", ")", "*", "3", ")"])
        self.assertEqual(result, ["1", "2", "+", "3", "*"])

    def test_complex_expression(self):
        """Complex expression"""
        # 2 + 3 * (4 - 1) ^ 2 → 2 3 4 1 - 2 ^ * +
        tokens = ["2", "+", "3", "*", "(", "4", "-", "1", ")", "^", "2"]
        expected = ["2", "3", "4", "1", "-", "2", "^", "*", "+"]
        self.assertEqual(infix_to_rpn(tokens), expected)

    def test_all_priority_levels(self):
        """All priority level"""
        # 1 + 2 * 3 ^ 2 → 1 2 3 2 ^ * +
        tokens = ["1", "+", "2", "*", "3", "^", "2"]
        expected = ["1", "2", "3", "2", "^", "*", "+"]
        self.assertEqual(infix_to_rpn(tokens), expected)

    def test_modulo_operator(self):
        """% operator"""
        # 10 % 3 + 2 → 10 3 % 2 +
        self.assertEqual(
            infix_to_rpn(["10", "%", "3", "+", "2"]), ["10", "3", "%", "2", "+"]
        )


class TestEvalRPN(unittest.TestCase):
    """Tests evaluating OPN"""

    def test_single_number(self):
        """One number"""
        self.assertEqual(eval_rpn(["5"]), 5.0)

    def test_addition(self):
        """Addition"""
        self.assertEqual(eval_rpn(["2", "3", "+"]), 5.0)

    def test_subtraction(self):
        """Substraction"""
        self.assertEqual(eval_rpn(["5", "3", "-"]), 2.0)

    def test_multiplication(self):
        """Multiplication"""
        self.assertEqual(eval_rpn(["4", "3", "*"]), 12.0)

    def test_division(self):
        """Division"""
        self.assertEqual(eval_rpn(["10", "2", "/"]), 5.0)

    def test_power(self):
        """Power"""
        self.assertEqual(eval_rpn(["2", "3", "^"]), 8.0)
        self.assertEqual(eval_rpn(["3", "2", "^"]), 9.0)

    def test_modulo(self):
        """% operator"""
        self.assertEqual(eval_rpn(["10", "3", "%"]), 1.0)

    def test_complex_rpn(self):
        """Complex rpn expression"""
        # 2 3 4 1 - 2 ^ * + = 29
        rpn = ["2", "3", "4", "1", "-", "2", "^", "*", "+"]
        self.assertEqual(eval_rpn(rpn), 29.0)

    def test_decimal_result(self):
        """Decimal result"""
        self.assertEqual(eval_rpn(["5", "2", "/"]), 2.5)

    def test_negative_result(self):
        """Negative result"""
        self.assertEqual(eval_rpn(["3", "5", "-"]), -2.0)


class TestCalculate(unittest.TestCase):
    """Test Calculate"""

    def test_simple_addition(self):
        """Addition"""
        self.assertEqual(calculate("2 + 3"), 5)

    def test_simple_multiplication(self):
        """Multiplication"""
        self.assertEqual(calculate("4 * 5"), 20)

    def test_priority_operations(self):
        """Priority"""
        self.assertEqual(calculate("2 + 3 * 4"), 14)
        self.assertEqual(calculate("10 - 2 * 3"), 4)

    def test_brackets(self):
        """Brackets"""
        self.assertEqual(calculate("(2 + 3) * 4"), 20)
        self.assertEqual(calculate("2 + (3 * 4)"), 14)

    def test_three_priority_levels(self):
        """All 3 priority"""
        # ^ (3) > * (2) > + (1)
        self.assertEqual(calculate("2 + 3 * 4 ^ 2"), 50)  # 2 + 3 * 16 = 50

    def test_complex_expression(self):
        """Complex expression"""
        self.assertEqual(calculate("2 + 3 * (4 - 1) ^ 2"), 29)

    def test_division(self):
        """Division"""
        self.assertEqual(calculate("10 / 2"), 5)
        self.assertEqual(calculate("7 / 2"), 3.5)

    def test_modulo(self):
        """% operator"""
        self.assertEqual(calculate("10 % 3"), 1)

    def test_power(self):
        """Power"""
        self.assertEqual(calculate("2 ^ 3"), 8)
        self.assertEqual(calculate("2 ^ 10"), 1024)

    def test_nested_brackets(self):
        """Nested brackets"""
        self.assertEqual(calculate("((2 + 3) * 4)"), 20)
        self.assertEqual(calculate("(1 + 2) * (3 + 4)"), 21)

    def test_spaces_handling(self):
        """Spaces handling"""
        self.assertEqual(calculate("  2  +  3  "), 5)
        self.assertEqual(calculate("2+3"), 5)

    def test_decimal_numbers(self):
        """Decimal numbers"""
        result = calculate("2.5 + 3.5")
        self.assertEqual(result, 6)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases"""

    def test_zero_operations(self):
        """Zero operations"""
        self.assertEqual(calculate("0 + 5"), 5)
        self.assertEqual(calculate("5 * 0"), 0)
        self.assertEqual(calculate("0 ^ 5"), 0)

    def test_large_numbers(self):
        """Big numbers"""
        self.assertEqual(calculate("1000 + 2000"), 3000)
        self.assertEqual(calculate("100 * 100"), 10000)

    def test_consecutive_operations(self):
        """consecutive operations w/ one priority level"""
        self.assertEqual(calculate("1 + 2 + 3"), 6)
        self.assertEqual(calculate("10 - 5 - 2"), 3)
        self.assertEqual(calculate("2 * 3 * 4"), 24)

    def test_mixed_operations(self):
        """Mixed operations"""
        self.assertEqual(calculate("10 + 5 * 2 - 3"), 17)
        self.assertEqual(calculate("100 / 10 + 5 * 2"), 20)

if __name__ == "__main__":
    # Запуск всех тестов
    unittest.main(verbosity=2)
