import unittest
from calculator import Calculator, Parser, Manager


class CalculatorTestCase(unittest.TestCase):
    """
    Contains test for calculator
    """
    def test_errors(self):
        calculator = Manager()

        errors = {"12+r": "UnknownSignError", "5/(2+(2*2)-6)": "ZeroDivisionError"}
        for expression in errors:
            self.assertEqual(calculator.calculation(expression), errors[expression])

    def test_simple(self):
        calculator = Manager()

        simple = {"2+2": 4, "6-5": 1, "-5+6": 1, "2*4": 8, "10/2": 5, "5^3": 125, "25*10^10": 250000000000}
        for expression in simple:
            self.assertEqual(calculator.calculation(expression), simple[expression])

    def test_normal(self):
        calculator = Manager()

        normal = {"2+2*2": 6, "(2+2)*2": 8, "6^0": 1, "5+4^6": 4101, "3^(2/2)": 3, "2+2*(2+2*2)": 14}
        for expression in normal:
            self.assertEqual(calculator.calculation(expression), normal[expression])

    def test_difficult(self):
        calculator = Manager()

        difficult = {"5+7^(2+4)": 117654, "54/2*9-1^9": 242, "56*4^9+25*(4-9)": 14679939}
        for expression in difficult:
            self.assertEqual(calculator.calculation(expression), difficult[expression])

    def test_float(self):
        calculator = Manager()

        expressions = {"2.9^5": 205.11148999999997, "4.9+(2.6-1.2/2)": 6.9, "2.5-0.5": 2}
        for expression in expressions:
            self.assertEqual(calculator.calculation(expression), expressions[expression])

    def test_trigonometry(self):
        calculator = Manager()

        expressions = {"cos(1+4)": 0.283662, "(3+2)+sin(19)": 5.149877,
                       "tg(3*7)": -1.527499}

        for expression in expressions:
            self.assertEqual(calculator.calculation(expression), expressions[expression])

if __name__ == "__main__":
    unittest.main()