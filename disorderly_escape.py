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
    if w == 0 or h == 0:
        return 1
    total = 0
    for i in range(1, w + 1):
        for j in range(1, h + 1):
            p = (s ** gcd(i, j))
            s2, s1 = symp(h - j, i, s), symp(w - i, j, s)
            prev = f(w - i, h - j, s)
            term = p * s1 * s2 * prev
            total += term
            if w == 2 and h == 3:
                print(i, j, p, s1, s2, prev, term)
    return total / (w * h)


def symp(n, k, s):
    if n == 0 or k == 0:
        return 1
    total = 0
    for i in range(1, n + 1):
        term = (s ** gcd(i, k)) * symp(n - i, k, s)
        total += term
    return total / n


def symmetric_orbits(n, s):
    if n == 0:
        return 1
    total = 0
    for i in range(n):
        total += s * symmetric_orbits(i, s)
    return total / n
