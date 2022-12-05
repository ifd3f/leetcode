#!/usr/bin/env python3

import re

with open('input') as f:
    lines = list(f)

i_moves = lines.index('\n')

stacks = [[] for _ in lines[i_moves - 1].split()]
for l in lines[:i_moves - 1]:
    for i, s in enumerate(stacks):
        char_index = i * 4 + 1
        char = l[char_index]
        if char == ' ':
            continue
        
        s.append(char)

stacks_expr = (
    'list<\n' +
    (',\n'.join([
        '    list<\n' +
        (',\n'.join([f"        charbox<'{c}'>" for c in s])) +
        '\n    >'
        for s in stacks
    ])) +
    '\n>'
)

moves = []
for m in lines[i_moves + 1:]:
    m = re.match(r'move (\d+) from (\d+) to (\d+)', m)
    n, f, t = map(int, m.groups())
    moves.append((n, f, t))

moves_expr = (
    'list<\n' +
    ',\n'.join([f'    move<{n}, {f}, {t}>' for n, f, t in moves]) +
    '\n>'
)

result = f'''#pragma once
#include "util.hpp"

using initial_stacks = {stacks_expr};

using moves_list = {moves_expr};
'''

with open('input.hpp', 'w') as f:
    f.write(result)

