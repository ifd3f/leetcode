def iterate(a, b):
    if a == b:
        return a, b

    b -= a
    a *= 2
    if a > b:
        a, b = b, a

    return a, b


def is_end(pair):
    a, b = pair
    return a == b


def is_infinite_cycle(a, b):
    """
    For 2 trainers with `a` and `b` bananas, do they undergo an infinite cycle?
    """
    visited = set()
    if a > b:
        a, b = b, a

    tortoise = a, b
    hare = iterate(a, b)
    while True:
        if tortoise == hare:
            return True
        if is_end(tortoise) or is_end(hare):
            return False
        tortoise = iterate(*tortoise)
        hare = iterate(*iterate(*hare))


def edge(a, b):
    if a > b:
        return b, a
    return a, b


class NormalNode(object):
    def __init__(self):
        self.neighbors = []

    def get_neighbors(self):
        return self.neighbors


class ContractedBlossomNode(object):
    def get_neighbors(self):
        pass


# adjacency: List[Set[int]]
# matching: Set[int]

def contract(nodes, adjacency):
    edges = {}
    for node in nodes:



def find_augmenting_path(adjacency, matching):
    forest = []
    unmarked_verts = set(range(len(adjacency)))
    marked_edges = set(matching)

    # Build set of exposed vertices
    exposed = set(range(len(adjacency)))
    for a, b in matching:
        if a in exposed:
            exposed.remove(a)
        if b in exposed:
            exposed.remove(b)

    for vertex in exposed:
        forest.append([vertex])

    while len(unmarked_verts) > 0:
        unmarked_verts


def find_maximum_matching(adjacency, matching):
    p = find_augmenting_path(adjacency, matching)
    pass


def build_graph(xs):
    i_to_adjacency = []
    for i, a in enumerate(xs):
        adjacencies = set()
        for j, b in enumerate(xs):
            if is_infinite_cycle(a, b):
                adjacencies.add(j)
        i_to_adjacency.append(adjacencies)
    return i_to_adjacency


def solution(bananas):
    i_to_adjacency = build_graph(bananas)

    for i in range(len(bananas)):
        for j in range(i):
            pass
