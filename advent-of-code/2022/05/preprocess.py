#!/usr/bin/env python3

import re

with open('input') as f:
    stack = []
    lines = [l.strip() for l in f]


i_moves = lines.index('')

moves = []
for m in lines[i_moves + 1:]:
    m = re.match(r'move (\d+) from (\d+) to (\d+)', m)
    n, f, t = map(int, m.groups())
    moves.append((n, f, t))


with open('input.hpp', 'w') as o:
    pass
