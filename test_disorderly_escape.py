import unittest

from disorderly_escape import *


class TestHelpers(unittest.TestCase):
    def test_symmetric_s2(self):
        self.assertEqual(3, symmetric_orbits(2, 2))

    def test_symmetric_s3(self):
        self.assertEqual(10, symmetric_orbits(3, 3))

    def test_1_row_grid(self):
        self.assertEqual(10, f(1, 3, 3))

    def test_0_row_grid(self):
        self.assertEqual(10, f(0, 3, 3))


class TestSolution(unittest.TestCase):
    def test_case_1(self):
        self.assertEqual('430', solution(2, 3, 4))

    def test_case_2(self):
        self.assertEqual('7', solution(2, 2, 2))


if __name__ == '__main__':
    unittest.main()
