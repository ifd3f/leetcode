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


def helper(m, terminals, count, offset, probs):
    # Note that m :: node -> neighbor -> flow from node to neighbor

    # Helper, because there's lots of possible early-return points
    def recurse():
        helper(m, terminals, count - 1, offset + 1, probs)

    row = m[offset]

    # Base case. Nothing to be done, since outputs[offset] = the end result.
    if count == 1:
        if not check_is_terminal(offset, row):
            probs[offset] = None
        return

    if check_is_terminal(offset, row):
        return recurse()

    # If it only self-loops, then this is a terminal node.
    self_flow = row[offset]
    if self_flow == 1:
        return recurse()

    # Normalize flows by removing self-loop, and check if this is a terminal state.
    factor = 1 / (1 - self_flow)
    for i in range(count):
        oi = offset + i
        value = row[oi]
        if value != 0:
            row[oi] = factor * value

    # Move this row's probability and flows to other rows.
    prob = probs[offset]
    probs[offset] = None  # Signal that this is a non-terminal row
    for i in range(1, count):
        oi = offset + i
        flow = row[oi]
        probs[oi] += flow * prob  # Move this state's probability to the other state's probability

        # Propagate every flow from other nodes through this node.
        for j in range(1, count):
            oj = offset + j
            m[oj][oi] += m[oj][offset] * flow  # Move this row's flow to other row's flows

    return recurse()


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

    # Initialize output matrix
    probabilities = [0] * count
    probabilities[0] = 1

    terminals = [check_is_terminal(i, row) for i, row in enumerate(m)]

    # Fraction-ize the matrix
    for row in m:
        denominator = sum(row)
        if denominator == 0:
            continue
        for i in range(len(row)):
            row[i] = Fraction(row[i], denominator)

    # Run tail-recursive helper
    helper(m, terminals, count, 0, probabilities)

    # Get output in the format wanted
    terminals = filter(lambda x: x is not None, probabilities)

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
