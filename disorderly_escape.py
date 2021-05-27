from fractions import gcd


def gcd2(a, b):
    if a == 0 and b == 0:
        return 1
    return gcd(a, b)


def lcm(a, b):
    return (a * b) / gcd(a, b)


def solution(w, h, s):
    return str(f(w, h, s))


def f(w, h, s):
    return SymmetricSymmetricProduct(w, h, s)(w, h)


class SymmetricSymmetricProduct(object):
    def __init__(self, w_max, h_max, s):
        self.data = [[1] * (w_max + 1) for i in range(h_max + 1)]
        self.s = s
        m = max(w_max, h_max)
        self.symp = SymmetricMonomialProduct(m, m, s)
        for w in range(1, w_max + 1):
            for h in range(1, h_max + 1):
                self.data[h][w] = self.calculate(w, h)

    def __call__(self, w, h):
        return self.data[h][w]

    def calculate(self, w, h):
        total = 0
        for i in range(1, w + 1):
            for j in range(1, h + 1):
                p = (self.s ** gcd(i, j))
                s2, s1 = self.symp(h - j, i), self.symp(w - i, j)
                prev = self.data[h - j][w - i]
                term = p * s1 * s2 * prev
                total += term
                if w == 2 and h == 3:
                    print(i, j, p, s1, s2, prev, term)
        return total / (w * h)


def symp(n, k, s):
    return SymmetricMonomialProduct(n, k, s)(n, k)


class SymmetricMonomialProduct(object):
    def __init__(self, n_max, k_max, s):
        self.data = [[1] * (k_max + 1) for i in range(n_max + 1)]
        self.s = s
        for n in range(1, n_max + 1):
            for k in range(1, k_max + 1):
                self.data[n][k] = self.calculate(n, k)

    def __call__(self, n, k):
        return self.data[n][k]

    def calculate(self, n, k):
        total = 0
        for i in range(1, n + 1):
            term = (self.s ** gcd(i, k)) * self.data[n - i][k]
            total += term
        return total / n


def symmetric_orbits(n, s):
    if n == 0:
        return 1
    total = 0
    for i in range(n):
        total += s * symmetric_orbits(i, s)
    return total / n


def grid_print(xss):
    strs = [[str(x) for x in xs] for xs in xss]
    cell_length = max((len(s) for row in strs for s in row)) + 1
    for row in strs:
        for cell in row:
            print cell.ljust(cell_length, ' '),
        print


if __name__ == '__main__':
    ssp = SymmetricSymmetricProduct(3, 3, 2)
    grid_print(ssp.data)
