from collections import defaultdict
from math import lcm

def getKey(p):
    x, y = p
    if x == 0:
        if y == 0:
            return None
        return 0, 1
    if y == 0:
        return 1, 0
    d = gcd(x, y)
    return abs(x) // d, abs(y) // d, (x > 0) == (y > 0)

def maxLineThroughPoint(ps, ref):
    index = defaultdict(list)
    px, py = ps[ref]
    origin = 1
    for i, (x, y) in enumerate(ps):
        if i == ref:
            continue
        o = (x - px, y - py)
        key = getKey(o)
        if key is None:
            origin += 1
        else:
            index[key].append(o)
    print(origin, index)
    if len(index) == 0:
        return origin
    return max(len(x) for x in index.values()) + origin

class Solution:
    def maxPoints(self, points: List[List[int]]) -> int:
        if len(points) <= 2:
            return len(points)
        return max(maxLineThroughPoint(points, i) for i in range(len(points)))
        