def solution(l):
    number_of_factors = [0] * len(l)  # map of index -> how many numbers before this index are factors?

    triples = 0

    # O(n^2) check to count factors
    for i, n in enumerate(l):
        for j in range(i):
            other = l[j]

            # does n divide other?
            if n % other == 0:
                triples += number_of_factors[j]
                number_of_factors[i] += 1

    return triples


if __name__ == '__main__':
    print solution([1, 2, 3, 4, 5, 6])  # 3
    print solution([1, 1, 1])  # 1

    # I suppose this one is supposed to count [1, 1, 2] multiple times?
    print solution([1, 1, 1, 2, 2])  # 10, or 4?
