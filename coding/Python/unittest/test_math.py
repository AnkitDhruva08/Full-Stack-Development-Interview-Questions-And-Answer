import unittest

def multiply(a, b):
    return a * b

class TestMath(unittest.TestCase):
    def test_multiply(self):
        self.assertEqual(multiply(3, 4), 12)
        self.assertNotEqual(multiply(2, 5), 20)

if __name__ == "__main__":
    unittest.main()
