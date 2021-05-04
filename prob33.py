import fractions
from fractions import Fraction


def check_is_terminal(offset, row):
    """
    A row is terminal if:
    - it is zero, OR
    - it only flows into itself.

    Therefore, a row is terminal if every value that is not self-flow is zero.
    """
    return all((x == 0) for x in row[:offset]) and all((x == 0) for x in row[offset + 1:])


def normalize_denominator(fs):
    if len(fs) == 1:
        return [fs[0].numerator, fs[0].denominator]

    common = fs[0].denominator

    for i in range(1, len(fs)):
        other = fs[i].denominator
        common = common * other / fractions.gcd(common, other)

    outputs = [f.numerator * common / f.denominator for f in fs]
    outputs.append(common)
    return outputs


def solution(m):
    count = len(m)

    # Fraction-ize the matrix
    for i, row in enumerate(m):
        denominator = sum(row)

        # This row is full of 0s. Convert it into a proper markov row.
        if denominator == 0:
            row[i] = 1
            continue

        # This row is nonzero. Convert everything into fractions.
        for j in range(len(row)):
            row[j] = Fraction(row[j], denominator)

    # Find terminal and transient states
    is_terminal = [check_is_terminal(i, row) for i, row in enumerate(m)]
    absorbing_is = [i for i in range(count) if is_terminal[i]]
    transient_is = [i for i in range(count) if not is_terminal[i]]

    # Initialize output matrix
    probs = [0] * count
    probs[0] = 1

    for node_i in transient_is:
        node_row = m[node_i]

        # This node may flow into itself. Normalize flows by removing self-loop.
        self_flow = node_row[node_i]
        if self_flow > 0:
            node_row[node_i] = 0
            norm_factor = 1 / (1 - self_flow)
            for i in range(count):
                node_row[i] *= norm_factor

        # Propagate probability from this node to other nodes.
        prob = probs[node_i]
        probs[node_i] = 0  # Null this row's probability
        for j in range(count):
            probs[j] += node_row[j] * prob

        # Add the outer product between column and row. Because the column represents ingress, and the row
        # represents egress, column * row = net effect, or the total propogation from others through this node.
        for j in range(count):
            for k in range(count):
                outer_product = m[j][node_i] * m[node_i][k]
                m[j][k] += outer_product

        # Null this row and column.
        for j in range(count):
            m[node_i][j] = 0
            m[j][node_i] = 0

    # Gather probabilities of absorbing states
    terminals = [probs[i] for i in absorbing_is]
    out = normalize_denominator(terminals)

    return out


def debug_matrix(m):
    for row in m:
        s = '\t'.join(map(str, row))
        print(s)
    print


import random


def generate_matrix(s):
    m = [
        [random.randint(0, 100) for _ in range(s)]
        for _ in range(s)
    ]
    for r in range(random.randint(1, s)):
        for i in range(s):
            m[r][i] = 0
    return m


def regular_tests():
    m0 = [
        [0, 1, 0, 0, 0, 1],  # s0, the initial state, goes to s1 and s5 with equal probability
        [4, 0, 0, 3, 2, 0],  # s1 can become s0, s3, or s4, but with different probabilities
        [0, 0, 0, 0, 0, 0],  # s2 is terminal, and unreachable (never observed in practice)
        [0, 0, 0, 0, 0, 0],  # s3 is terminal
        [0, 0, 0, 0, 0, 0],  # s4 is terminal
        [0, 0, 0, 0, 0, 0],  # s5 is terminal
    ]
    sol1 = solution(m0)
    assert sol1 == [0, 3, 2, 9, 14]

    assert solution([
        [0, 0],
        [0, 24]
    ]) == [1, 0, 1]
    assert len(solution([
        [0, 0, 0, 0],
        [1, 1, 0, 1],
        [0, 0, 0, 0],
        [1, 1, 0, 1]
    ])) == 3
    assert len(solution(
        [[0, 0, 0, 0, 0, 0, 0], [32, 36, 27, 64, 49, 87, 52], [47, 27, 60, 84, 81, 17, 100], [0, 0, 0, 0, 0, 0, 0],
         [89, 77, 63, 76, 32, 80, 36], [0, 0, 0, 0, 0, 0, 0], [90, 90, 21, 98, 48, 78, 80]])) == 4
    assert solution([
        [0, 0, 0],
        [1, 0, 0],
        [0, 0, 0]
    ]) == [1, 0, 1]
    assert solution([
        [0, 0, 1],
        [1, 0, 0],
        [0, 0, 0]
    ]) == [1, 1]
    assert solution([
        [0, 1, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]) == [1, 0, 1]
    assert solution([
        [0, 0, 1],
        [0, 0, 0],
        [0, 0, 0]
    ]) == [0, 1, 1]
    assert solution([[0]]) == [1, 1]
    assert solution([[0, 0], [0, 0]]) == [1, 0, 1]
    assert solution([
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]) == [1, 0, 0, 1]

    assert solution([[3]]) == [1, 1]

    assert solution([
        [0, 2, 1, 0, 0],
        [0, 0, 0, 3, 4],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]) == [7, 6, 8, 21]

    print solution([
        [0, 1, 2, 0, 0],
        [1, 0, 1, 1, 0],
        [1, 1, 0, 0, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ])

    print solution([
        [9, 1, 2, 0, 8],
        [1, 3, 1, 1, 0],
        [1, 1, 9, 0, 1],
        [0, 0, 0, 0, 0],
        [2, 3, 4, 1, 0]
    ])


if __name__ == '__main__':
    regular_tests()

    import copy

    for i in range(10000):
        m = generate_matrix(random.randint(1, 10))
        terms = 0
        for i, row in enumerate(m):
            if all((x == 0) for x in row[:i]) and all((x == 0) for x in row[i + 1:]):
                terms += 1
        m2 = copy.deepcopy(m)
        sol = solution(m2)

        assert terms + 1 == len(sol)
