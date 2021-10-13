import unittest

from disorderly_escape import *


def symmetric_orbits(n, s):
    if n == 0:
        return 1
    total = 0
    for i in range(n):
        total += s * symmetric_orbits(i, s)
    return total / n


def symmetric_group(n):
    return symmetric_group_cycle_indices(n)[n]


class TestMonomial(unittest.TestCase):
    def test_monomial_hashes_correctly(self):
        m1 = Mono({5: 3, 3: 2, 6: 5})
        m2 = Mono(Counter({3: 2, 6: 5, 5: 3}))

        h1, h2 = hash(m1), hash(m2)

        self.assertEqual(h1, h2)

    def test_cycle_cartesian_1(self):
        m1 = Mono({3: 1})
        m2 = Mono({6: 1})
        actual = Mono({6: 3})

        prod = m1 & m2

        self.assertEqual(actual, prod)


class TestPolynomial(unittest.TestCase):
    def test_symmetric_group_2(self):
        p1 = symmetric_group(2)

        actual = Poly({Mono({1: 2}): Fraction(1, 2), Mono({2: 1}): Fraction(1, 2)})
        self.assertEqual(actual, p1)

    def test_symmetric_group_3(self):
        p1 = symmetric_group(3)

        actual = Poly({Mono({3: 1}): Fraction(1, 3), Mono({1: 1, 2: 1}): Fraction(1, 2), Mono({1: 3}): Fraction(1, 6)})
        self.assertEqual(actual, p1)

    def test_cycle_cartesian_1(self):
        p1 = symmetric_group(2)

        prod = p1 & p1

        actual = Poly({Mono({1: 4}): Fraction(1, 4), Mono({2: 2}): Fraction(3, 4)})
        self.assertEqual(actual, prod)

    def test_cycle_cartesian_2(self):
        p1 = symmetric_group(2)
        p2 = symmetric_group(3)

        prod = p1 & p2

        actual = Poly({
            Mono({1: 6}): Fraction(1, 12),
            Mono({2: 3}): Fraction(1, 3),
            Mono({1: 2, 2: 2}): Fraction(1, 4),
            Mono({3: 2}): Fraction(1, 6),
            Mono({6: 1}): Fraction(1, 6),
        })
        self.assertEqual(actual, prod)


class TestSolution(unittest.TestCase):
    def test_case_1(self):
        self.assertEqual('430', solution(2, 3, 4))

    def test_case_2(self):
        self.assertEqual('7', solution(2, 2, 2))


if __name__ == '__main__':
    unittest.main()
