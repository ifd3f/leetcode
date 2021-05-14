import unittest

from distract_the_trainers import is_infinite_cycle, solution


class MyTestCase(unittest.TestCase):
    def test_infinite_cycle(self):
        self.assertTrue(is_infinite_cycle(1, 4))

    def test_case_1(self):
        self.assertEqual(2, solution([1, 1]))

    def test_case_2(self):
        self.assertEqual(0, solution([1, 7, 3, 21, 13, 19]))


if __name__ == '__main__':
    unittest.main()
