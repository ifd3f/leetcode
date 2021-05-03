from collections import defaultdict, Counter


def solution(l):
    counts = list(Counter(l).items())

    number_of_factors = [0] * len(counts)  # map of number -> how many factors it has
    triples = 0

    for i, (n, n_count) in enumerate(counts):
        if n_count >= 2:
            # double-counting
            number_of_factors[i] += 1
        if n_count >= 3:
            triples += 1

        for j in range(i):
            other, other_count = counts[j]

            # does n divide other?
            if n % other == 0:
                # can we double-count n?
                if n_count >= 2:
                    triples += 1
                triples += number_of_factors[j]
                number_of_factors[i] = number_of_factors[i] + 1
    return triples
