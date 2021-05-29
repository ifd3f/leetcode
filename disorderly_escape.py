from collections import Counter, defaultdict
from fractions import gcd, Fraction


def prod(iterable):
    p = 1
    for x in iterable:
        p *= x
    return p


def gcd2(a, b):
    if a == 0 and b == 0:
        return 1
    return gcd(a, b)


def lcm(a, b):
    return (a * b) / gcd(a, b)


def solution(w, h, s):
    return str(f(w, h, s))


class Mono(object):
    def __init__(self, factors):
        self.factors = factors
        self.hash = None

    def __repr__(self):
        return 'Mono(' + repr(dict(self.factors)) + ')'

    def __str__(self):
        return ' '.join('a_{%s}^{%s}' % (s, p) for s, p in self.factors.items())

    def __eq__(self, other):
        return self.factors == other.factors

    def __hash__(self):
        if self.hash is None:
            self.hash = 0
            factors = list(self.factors)
            factors.sort()
            for b in factors:
                p = self.factors[b]
                self.hash <<= 3
                self.hash %= 2 ** 31
                self.hash += b * p
        return self.hash

    def is_one(self):
        return all((p == 0 for _, p in self.factors.items()))

    def __mul__(self, other):
        assert isinstance(other, Mono), "Can only multiply monomials with monomials"
        if other.is_one():
            return self
        if self.is_one():
            return other
        return Mono(Counter(self.factors) + Counter(other.factors))

    def cycle_cartesian(self, other):
        assert isinstance(other, Mono), "Can only multiply monomials with monomials"
        if other.is_one() or self.is_one():
            return CIM_ONE
        result = Counter()
        for f1, p1 in self.factors.items():
            for f2, p2 in other.factors.items():
                g = gcd(f1, f2)
                a_pow = g * p1 * p2
                a_sub = (f1 * f2) / g
                result[a_sub] += a_pow
        return Mono(result)

    def substitute(self, s):
        return prod((a ** p for a, p in self.factors.items()))


CIM_ONE = Mono({})


class Poly(object):
    def __init__(self, monomials):
        self.monomials = monomials

    def __repr__(self):
        return 'Poly(' + repr(dict(self.monomials)) + ')'

    def __eq__(self, other):
        return self.monomials == other.monomials

    @staticmethod
    def symmetric_group(n):
        symmetric_groups = [CIP_ZERO] * (n + 1)
        symmetric_groups[0] = Poly({CIM_ONE: 1})
        for m in range(1, n + 1):
            poly_sum = CIP_ZERO
            for i in range(1, m + 1):
                mono = Mono({i: 1})
                poly = Poly({mono: 1})
                zs = symmetric_groups[m - i]
                term = zs.multiply(poly)
                poly_sum += term
            symmetric_groups[m] = poly_sum.scale(Fraction(1, m))
        return symmetric_groups[n]

    def __str__(self):
        return ' + '.join('%s %s' % (c, m) for m, c in self.monomials.items())

    def multiply(self, other):
        assert isinstance(other, Poly), "Can only multiply polynomials with polynomials"
        result = defaultdict(lambda: Fraction(0))
        for m1, c1 in self.monomials.items():
            for m2, c2 in other.monomials.items():
                monomial = m1 * m2
                coeff = c1 * c2
                result[monomial] += coeff
        return Poly(result)

    def __add__(self, other):
        result = defaultdict(lambda: Fraction(0))
        for m, c in self.monomials.items():
            result[m] += c
        for m, c in other.monomials.items():
            result[m] += c
        return Poly(result)

    def scale(self, scalar):
        return Poly({
            m1: c1 * scalar for m1, c1 in self.monomials.items()
        })

    def cycle_cartesian(self, other):
        assert isinstance(other, Poly), "Can only multiply polynomials with polynomials"
        result = defaultdict(lambda: Fraction(0))
        for m1, c1 in self.monomials.items():
            for m2, c2 in other.monomials.items():
                monomial = m1.cycle_cartesian(m2)
                coeff = c1 * c2
                result[monomial] += coeff
        return Poly(result)

    def substitute(self, s):
        return prod((c * m.substitute(s) for m, c in self.monomials.items()))


CIP_ZERO = Poly({})


def grid_print(xss):
    strs = [[str(x) for x in xs] for xs in xss]
    cell_length = max((len(s) for row in strs for s in row)) + 1
    for row in strs:
        for cell in row:
            print cell.rjust(cell_length),
        print


if __name__ == '__main__':
    p1 = Poly.symmetric_group(2)
    p2 = Poly.symmetric_group(3)
    print repr(p1.cycle_cartesian(p1))

    print p1.cycle_cartesian(p2).substitute(2)
