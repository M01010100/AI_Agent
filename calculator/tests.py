
import unittest

class TestCalculator(unittest.TestCase):
    def test_add(self):
        self.assertEqual(1 + 1, 2)
    
    def test_subtract(self):
        self.assertEqual(5 - 3, 2)
    
    def test_multiply(self):
        self.assertEqual(2 * 3, 6)
    
    def test_divide(self):
        self.assertEqual(6 / 3, 2)
    
    def test_modulo(self):
        self.assertEqual(7 % 3, 1)
    
    def test_power(self):
        self.assertEqual(2 ** 3, 8)
    
    def test_floor_division(self):
        self.assertEqual(7 // 3, 2)
    
    def test_negative(self):
        self.assertEqual(-1 * 3, -3)
    
    def test_zero(self):
        self.assertEqual(0 * 5, 0)

if __name__ == '__main__':
    unittest.main()
