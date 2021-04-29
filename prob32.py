from collections import Counter


# builds dag of y in dag[x] if x divides y
def build_dag(l):
    l.sort(reverse=True)
    dag = {n: set() for n in l}

    max_mult = 0
    for small in range(len(l)):
        lsmall = l[small]
        squared = lsmall * lsmall
        while l[max_mult] > squared and max_mult > lsmall:
            max_mult += 1
        for big in range(max_mult, small):
            lbig = l[big]
            if lbig % lsmall == 0:
                dag[lsmall].add(lbig)

    return dag


def get_occurences(dag, counts, x, steps_away=3, used_x=1):
    if steps_away <= 1:
        return 1

    next_steps = steps_away - 1

    # We can still count this current node
    if counts[x] - used_x > 0:
        paths = get_occurences(dag, counts, x, next_steps, used_x + 1)
    else:
        paths = 0

    for y in dag[x]:
        paths += get_occurences(dag, counts, y, next_steps, 1)

    return paths


def solution(l):
    counts = Counter(l)
    unique = list(counts)
    dag = build_dag(unique)
    count = 0
    for x in unique:
        count += get_occurences(dag, counts, x)
    return count


if __name__ == '__main__':
    print solution([1, 2, 3, 4, 5, 6])
    print solution([1, 2, 3, 4, 5, 6, 7, 8])
    print solution([2, 3, 4, 5, 6, 7, 8])
    print solution([2, 3, 4, 5, 7, 8])
    print solution([8, 9, 10])
    print solution([1])
    print solution([1, 1])
    print solution([1, 1, 1, 2, 2, 2])
