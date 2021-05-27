import unittest

from disorderly_escape import *


class TestHelpers(unittest.TestCase):
    def test_symp_0(self):
        self.assertEqual(6, symp(1, 9, 6))

    def test_symp_1(self):
        self.assertEqual(36, symp(2, 2, 6))

    def test_symp_2(self):
        self.assertEqual(9, symp(2, 2, 3))

    def test_symp_3(self):
        self.assertEqual(10, symp(2, 3, 4))

    def test_symp_4(self):
        self.assertEqual(1, symp(4, 0, 4))

    def test_grid_0(self):
        self.assertEqual(1, f(0, 3, 3))

    def test_grid_1(self):
        self.assertEqual(10, f(1, 3, 3))

    def test_grid_2(self):
        self.assertEqual(13, f(2, 3, 2))

    def test_grid_3(self):
        self.assertEqual(430, f(2, 3, 4))

    def test_grid_4(self):
        self.assertEqual(10, f(1, 3, 3))

    def test_grid_5(self):
        self.assertEqual(3, f(1, 2, 2))

    def test_grid_6(self):
        self.assertEqual(4, f(1, 3, 2))


class TestSolution(unittest.TestCase):
    def test_case_1(self):
        self.assertEqual('430', solution(2, 3, 4))

    def test_case_2(self):
        self.assertEqual('7', solution(2, 2, 2))


if __name__ == '__main__':
    unittest.main()
