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
    if w == 0:
        return 1
    if h == 0:
        return 1
    total = 0
    for i in range(1, w + 1):
        for j in range(1, h + 1):
            term = (s ** gcd(i, j)) * f(w - i, h - j, s) * symp(h - j, i, s) * symp(w - i, j, s)
            total += term
            print(w, h, s, i, j, term)
    return total / (w * h)


def symp(n, k, s):
    if n == 0:
        return 1
    total = 0
    for i in range(1, n + 1):
        term = (s ** gcd(i, k)) * symp(n - i, k, s)
        print n, i, k, gcd(i, k), s, term
        total += term
    return total / n


def symmetric_orbits(n, s):
    if n == 0:
        return 1
    total = 0
    for i in range(n):
        total += s * symmetric_orbits(i, s)
    return total / n
