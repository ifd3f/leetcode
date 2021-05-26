from fractions import gcd


def lcm(a, b):
    return (a * b) / gcd(a, b)


def solution(w, h, s):
    return str(f(w, h, s))


def f(w, h, s):
    if w == 0:
        return symmetric_orbits(h, s)
    if h == 0:
        return symmetric_orbits(w, s)
    total = 0
    for i in range(1, w + 1):
        for j in range(1, h + 1):
            total += (s ** gcd(i, j)) * f(w - i, h - j, s)

    return total / (w * h)


def symmetric_orbits(n, s):
    if n == 0:
        return 1
    total = 0
    for i in range(n):
        total += s * symmetric_orbits(i, s)
    return total / n
