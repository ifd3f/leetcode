from collections import defaultdict


def is_infinite_cycle(a, b):
    """
    For 2 trainers with `a` and `b` bananas, do they undergo an infinite cycle?
    """

    # Is their sum a power of 2? (equivalent to the solution, as proved by modular arithmetic)
    s = a + b

    # Checking for power 2 https://stackoverflow.com/questions/57025836/how-to-check-if-a-given-number-is-a-power-of-two
    return (s & (s - 1) == 0) and s != 0


def mk_edge(a, b):
    return (b, a) if a > b else (a, b)


class Forest(object):
    def __init__(self):
        self.parents = dict()
        self.children = defaultdict(set)
        self.node_to_is_even = dict()

    def __contains__(self, item):
        return item in self.parents

    def is_even(self, n):
        return self.node_to_is_even[n]

    def set_parent(self, x, p):
        self.parents[x] = p
        self.children[p].add(x)
        if p is None:
            self.node_to_is_even[x] = False
        else:
            self.node_to_is_even[x] = not self.node_to_is_even[p]

    def get_children(self, x):
        return self.children[x]

    def get_parent(self, x):
        return self.parents[x]

    def get_root(self, x):
        while self.get_parent(x) is not None:
            x = self.get_parent(x)
        return x

    def get_path_to_root(self, x):
        while self.get_parent(x) is not None:
            yield x
            x = self.get_parent(x)


class Graph(object):
    def __init__(self):
        self.adjacency = defaultdict(set)
        self.is_even = defaultdict(lambda: None)

    def edges(self):
        es = set()
        for node, neighbors in self.adjacency.items():
            for neighbor in neighbors:
                edge = mk_edge(node, neighbor)
                if edge not in es:
                    yield edge
                    es.add(edge)

    def mate(self, n):
        """If this graph represents a matching, returns the given node's matched mate, or None."""
        neighbors = self.adjacency[n]
        assert len(neighbors) <= 1, "Invalid matching: %s has more than 1 neighbor" % n
        if len(neighbors) == 0:
            return None
        return next(iter(neighbors))  # take the only neighbor out

    def add_edge_tup(self, e):
        a, b = e
        self.adjacency[a].add(b)
        self.adjacency[b].add(a)

    def rm_edge_tup(self, e):
        a, b = e
        self.adjacency[a].remove(b)
        self.adjacency[b].remove(a)

    def exposed_vertices(self, matching):
        for node, neighbors in self.adjacency.items():
            if matching.mate(node) is None:
                yield node

    def find_augmenting_path(self, matching):
        # Resources:
        # https://en.wikipedia.org/wiki/Blossom_algorithm#Finding_an_augmenting_path
        # https://www.cs.tau.ac.il/~zwick/grad-algo-0910/match.pdf
        forest = Forest()
        marked_edges = set()
        marked_nodes = set()

        # Mark all edges of matching
        for edge in matching.edges():
            marked_edges.add(edge)

        # Use exposed nodes as roots of their own trees
        exposed_nodes = list(self.exposed_vertices(matching))
        for node in exposed_nodes:
            # Add node to forest
            forest.set_parent(node, None)

        # Explore the graph from the exposed nodes.
        for tree_root in exposed_nodes:
            # Use a DFS because it's easiest.
            search_stack = [tree_root]
            visited = set()
            while len(search_stack) > 0:
                # We want to find the next unmarked even vertex.
                # Perform the DFS step
                v = search_stack.pop()
                if v in visited:
                    continue
                visited.add(v)
                search_stack.extend(self.adjacency[v])

                if not forest.is_even(v):
                    continue

                # Now we know that v is even, look through its unmarked edges.
                for w in self.adjacency[v]:
                    # Exclude marked edges.
                    if mk_edge(v, w) in marked_edges:
                        continue

                    x = matching.mate(w)

                    # If w not in forest, then it is matched already.
                    if w not in forest:
                        forest.set_parent(w, v)
                        forest.set_parent(x, w)
                        continue

                    # If w is odd, do nothing
                    if not forest.is_even(w):
                        continue

                    # If x is None, then w is unmatched and exposed. We have found an augmented path from w to its root.
                    if x is None:
                        return list(forest.get_path_to_root(w))

                    # If v and w are different trees, we found an augmenting path.
                    if forest.get_root(v) != forest.get_root(w):
                        path_v = list(forest.get_path_to_root(v))
                        path_w = list(forest.get_path_to_root(w))
                        path_w.reverse()
                        return path_v + path_w

                    # If v and w are the same tree: blossom detected.
                    # TODO blossom code
                    # graph2 = deepcopy(self)
                    # matching2 = contract stuff
                    # graph2.find_augmenting_path()
                    assert False, "Blossom NYI"

        # No augmenting path has been found, so return a sentinel value.
        return None


def augment(path, matching):
    should_add = True
    for i in range(len(path) - 1):
        a = path[i]
        b = path[i + 1]

        if should_add:
            matching.add_edge_tup((a, b))
        else:
            matching.rm_edge_tup((a, b))

        i += 1
        should_add = not should_add


class Contraction(object):
    def __init__(self, graph, nodes, name):
        self.graph = graph
        self.contracted_nodes = nodes
        self.name = name
        self.removed_edges = None
        self.neighbors = None

    def __enter__(self):
        self.removed_edges = []
        self.neighbors = set()
        for node in self.contracted_nodes:
            for neighbor in self.graph.adjacency[node]:
                self.removed_edges.append((node, neighbor))
                self.neighbors.add(neighbor)

        for edge in self.removed_edges:
            self.graph.rm_edge_tup(edge)

        for neighbor in self.neighbors:
            self.graph.add_edge_tup((self.name, neighbor))

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is not None:
            raise exc_val

        for neighbor in self.neighbors:
            self.graph.rm_edge_tup((self.name, neighbor))

        for edge in self.removed_edges:
            self.graph.add_edge_tup(edge)


def find_maximum_matching(adjacency, matching):
    p = find_augmenting_path(adjacency, matching)
    pass


def build_graph(xs):
    graph = Graph()
    for i, a in enumerate(xs):
        for j in range(i):
            b = xs[j]
            if is_infinite_cycle(a, b):
                graph.add_edge_tup((i, j))
    return graph


def solution(bananas):
    graph = build_graph(bananas)
    print(graph.adjacency)

    for i in range(len(bananas)):
        for j in range(i):
            pass
