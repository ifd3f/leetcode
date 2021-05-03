import fractions
from fractions import Fraction
import math
from pprint import pprint


def debug_matrix(m):
    for row in m:
        s = '\t'.join(map(str, row))
        print(s)
    print


def helper(m, count, offset, outputs):
    # Note that m :: node -> neighbor -> flow

    # Base case. Nothing to be done, since outputs[offset] = the end result.
    if count == 1:
        return

    row = m[offset]

    # Normalize flows by removing self-loop, and check if this is a terminal state.
    self_flow = row[offset]
    factor = 1 / (1 - self_flow)
    is_terminal = True
    for i in range(count):
        oi = offset + i
        value = row[oi]
        if value != 0:
            is_terminal = False
            row[oi] = factor * value

    if not is_terminal:
        # Move this row's probability to other rows, scaled by flow.
        # Also, move this row's flows to other rows' identities.
        prob = outputs[offset]
        outputs[offset] = None  # Signal that this is a non-terminal row
        for i in range(1, count):
            oi = offset + i
            flow = row[oi]
            outputs[oi] += flow * prob  # Move this state's probability to the other state's probability

            for j in range(1, count):
                oj = offset + j
                m[oj][oi] += m[oj][offset] * flow  # Move this row's flow to other row's flows

    helper(m, count - 1, offset + 1, outputs)


def find_common_denominator(denominators):
    denominator = denominators[0]
    for i in range(1, len(denominators)):
        other = denominators[i]
        denominator = denominator * other / fractions.gcd(denominator, other)
    return denominator


def solution(m):
    count = len(m)

    # Initialize output matrix
    probabilities = [0] * count
    probabilities[0] = 1

    # Fraction-ize the matrix
    for row in m:
        denominator = sum(row)
        if denominator == 0:
            continue
        for i in range(len(row)):
            row[i] = Fraction(row[i], denominator)

    # Run recursive helper
    helper(m, count, 0, probabilities)

    # Get output in the format wanted
    terminals = filter(lambda x: x is not None, probabilities)
    denominator = find_common_denominator([f.denominator for f in terminals])
    outputs = [f.numerator * denominator / f.denominator for f in terminals]
    outputs.append(denominator)

    return outputs


if __name__ == '__main__':
    m0 = [
        [0, 1, 0, 0, 0, 1],  # s0, the initial state, goes to s1 and s5 with equal probability
        [4, 0, 0, 3, 2, 0],  # s1 can become s0, s3, or s4, but with different probabilities
        [0, 0, 0, 0, 0, 0],  # s2 is terminal, and unreachable (never observed in practice)
        [0, 0, 0, 0, 0, 0],  # s3 is terminal
        [0, 0, 0, 0, 0, 0],  # s4 is terminal
        [0, 0, 0, 0, 0, 0],  # s5 is terminal
    ]
    sol1 = solution(m0)
    print(sol1)
    assert sol1 == [0, 3, 2, 9, 14]

    assert solution([
        [0, 2, 1, 0, 0],
        [0, 0, 0, 3, 4],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]) == [7, 6, 8, 21]
