from collections import defaultdict
from copy import deepcopy


def is_infinite_cycle(a, b):
    """
    For 2 trainers with `a` and `b` bananas, do they undergo an infinite cycle?
    """

    # Is their sum a power of 2? (equivalent to the solution, as proved by modular arithmetic)
    s = a + b

    # Checking for power 2 https://stackoverflow.com/questions/57025836/how-to-check-if-a-given-number-is-a-power-of-two
    return not ((s & (s - 1) == 0) and s != 0)


def build_graph(xs):
    graph = Graph()
    for i, a in enumerate(xs):
        for j in range(i):
            b = xs[j]
            if is_infinite_cycle(a, b):
                graph.add_edge_tup((i, j))
    return graph


def mk_edge(a, b):
    """
    Convenient helper.
    :param a: one node
    :param b: another node
    :return: an edge tuple in standard form (where left < right)
    """
    return (b, a) if a > b else (a, b)


class Forest(object):
    """
    Represents a forest used in maximum matching search.
    """

    def __init__(self):
        self.parents = dict()
        self.node_to_is_even = dict()

    def __contains__(self, item):
        return item in self.parents

    def is_even(self, n):
        return self.node_to_is_even[n]

    def set_parent(self, x, p):
        self.parents[x] = p
        if p is None:
            self.node_to_is_even[x] = True
        else:
            self.node_to_is_even[x] = not self.node_to_is_even[p]

    def get_parent(self, x):
        return self.parents[x]

    def get_root(self, x):
        while self.get_parent(x) is not None:
            x = self.get_parent(x)
        return x

    def get_path_to_root(self, x):
        while x is not None:
            yield x
            x = self.get_parent(x)

    def get_path_from_child_to_parent(self, f, t):
        path = []
        while f != t:
            if f is None:
                return None
            path.append(f)
            f = self.get_parent(f)
        path.append(t)
        return path

    def find_common_ancestor(self, a, b):
        visited = set()
        while True:
            # No common ancestor
            if a is None and b is None:
                return None

            if a is not None:
                if a in visited:
                    return a
                visited.add(a)
                a = self.get_parent(a)
            if b is not None:
                if b in visited:
                    return b
                visited.add(b)
                b = self.get_parent(b)


class Graph(object):
    def __init__(self):
        self.adjacency = defaultdict(set)
        self.is_even = defaultdict(lambda: None)

    def __repr__(self):
        return 'Graph(%s)' % (' '.join(map(repr, self.edges())),)

    def edges(self):
        es = set()
        for node, neighbors in self.adjacency.items():
            for neighbor in neighbors:
                edge = mk_edge(node, neighbor)
                if edge not in es:
                    yield edge
                    es.add(edge)

    def edge_count(self):
        return sum(1 for _ in self.edges())

    def mate(self, n):
        """
        If this graph represents a matching, returns the given node's matched mate, or None.
        """
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

    def rm_node(self, node):
        # Remove references from others to this
        for neighbor in self.adjacency[node]:
            self.adjacency[neighbor].remove(node)
        # Remove this node
        del self.adjacency[node]

    def contract(self, nodes):
        """Contracts the given list of nodes, and returns the new node it was contracted to."""
        new_neighbors = set()
        for node in nodes:
            new_neighbors.union(self.adjacency[node])
        new_neighbors.difference(nodes)

        for node in nodes:
            self.rm_node(node)

        v_b = nodes[0]
        for neighbor in new_neighbors:
            self.add_edge_tup((v_b, neighbor))

        return v_b

    def exposed_vertices(self, matching):
        for node, neighbors in self.adjacency.items():
            if matching.mate(node) is None:
                yield node

    def generate_maximum_matching(self):
        """
        :return: a maximum matching of this graph.
        """

        # By Berge's lemma, a matching is maximum if it does not contain any augmenting paths. So, keep augmenting paths
        # as long as they exist.
        matching = Graph()
        while True:
            path = self.find_augmenting_path(matching)
            if path is None:
                break
            augment(path, matching)

        return matching

    def find_augmenting_path(self, matching):
        """
        Finds an augmenting path in this graph given the provided matching.
        :param matching: the matching, encoded as a Graph where the edges are the matches.
        :return: an augmenting path, or None if there are no augmenting paths in this graph.
        """

        # Resources used for this algorithm:
        # https://en.wikipedia.org/wiki/Blossom_algorithm#Finding_an_augmenting_path
        # https://www.cs.tau.ac.il/~zwick/grad-algo-0910/match.pdf
        forest = Forest()
        visited_edges = set()
        visited_nodes = set()

        # Mark all edges of matching
        for edge in matching.edges():
            visited_edges.add(edge)

        # Use exposed nodes as roots of their own trees
        exposed_nodes = list(self.exposed_vertices(matching))
        for node in exposed_nodes:
            # Add node to forest
            forest.set_parent(node, None)

        # Explore the graph from the exposed nodes.
        # Use a DFS because it's easiest.
        search_stack = list(exposed_nodes)
        while len(search_stack) > 0:
            # We want to find the next unmarked even vertex.
            # Perform the DFS step
            v = search_stack.pop()
            if v in visited_nodes:
                continue
            visited_nodes.add(v)

            # Skip v if it is not even
            if not forest.is_even(v):
                continue

            # Now we know that v is even, look through its unmarked edges.
            for w in self.adjacency[v]:
                # Exclude marked edges.
                edge = mk_edge(v, w)
                if edge in visited_edges:
                    continue
                search_stack.append(w)
                visited_edges.add(edge)

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
                    path = [w]
                    path.extend(forest.get_path_to_root(v))
                    return path

                # If v and w are different trees, we found an augmenting path.
                if forest.get_root(v) != forest.get_root(w):
                    path = list(forest.get_path_to_root(v))
                    path.reverse()
                    path.extend(forest.get_path_to_root(w))
                    return path

                # If v and w are the same tree: blossom detected. Find the nodes of this cycle.
                ancestor = forest.find_common_ancestor(v, w)
                path_v = forest.get_path_from_child_to_parent(v, ancestor)  # v -> root
                path_w = forest.get_path_from_child_to_parent(w, ancestor)  # w -> root
                full_cycle = path_v[::-1] + path_w[:-1]  # root -> v, then w -> excluding root

                # Perform a check on a contracted copy
                graph2 = deepcopy(self)
                matching2 = deepcopy(matching)
                matching2.contract(full_cycle)
                v_b = graph2.contract(full_cycle)
                contracted_path = graph2.find_augmenting_path(matching2)

                # No augmenting paths found
                if contracted_path is not None:
                    return self.lift_contracted_path(contracted_path, full_cycle, v_b)

        # No augmenting path has been found, so return a sentinel value.
        return None

    def lift_contracted_path(self, contracted_path, full_cycle, v_b):
        """
        Given a cycle that is contracted to v_b, and a contracted path that has that cycle, lift the path to the full
        graph.
        :param contracted_path:
        :param full_cycle: the cycle, with element 0 being a node marked as "even" in the forest.
        :param v_b:
        :return:
        """
        # To make the code more organized, v_b must not be the last node of the path.
        if contracted_path[-1] == v_b:
            contracted_path.reverse()
        i_v_b = contracted_path.index(v_b)

        # We found an augmenting path without the contracted blossom, so no lifting needed.
        if i_v_b is None:
            return contracted_path

        # Otherwise, the contracted path goes through the contracted blossom.
        intra_cycle = self.get_intra_cycle_path(contracted_path, full_cycle, i_v_b)

        # Concatenate the paths!
        return contracted_path[:i_v_b] + intra_cycle + contracted_path[i_v_b + 1:]

    def get_intra_cycle_path(self, contracted_path, full_cycle, i_v_b):
        """
        Given a cycle that is contracted to v_b, and a contracted path that has that cycle at index i_v_b, find the path
        within the cycle that should replace v_b in the contracted_cycle to expand it to the full graph.
        :param contracted_path:
        :param full_cycle: the cycle, with element 0 being a node marked as "even" in the forest.
        :param i_v_b: index of v_b in contracted_path
        :return:
        """

        # If the path does not begin in the cycle, rotate the cycle so that element 0 is where the contracted
        # path enters the cycle. This reduces the amount of messy if-statements later on.
        if i_v_b != 0:
            v_entry = contracted_path[i_v_b - 1]
            v_cycle_entry = next((n for n in self.adjacency[v_entry] if n in full_cycle))
            i_cycle_entry = full_cycle.index(v_cycle_entry)
            full_cycle = full_cycle[i_cycle_entry:] + full_cycle[:i_cycle_entry]

        # Find exit index in this cycle
        v_exit = contracted_path[i_v_b + 1]
        v_cycle_exit = next((n for n in self.adjacency[v_exit] if n in full_cycle))
        i_cycle_exit = full_cycle.index(v_cycle_exit)

        # Given the in-cycle exit, find the route from the entry point to the exit point that would be even.
        if i_cycle_exit % 2 == 0:
            intra_cycle = full_cycle[:i_cycle_exit + 1]
        else:
            intra_cycle = full_cycle[i_cycle_exit:]
            intra_cycle.append(full_cycle[0])
            intra_cycle.reverse()
        return intra_cycle


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


def solution(bananas):
    graph = build_graph(bananas)
    maximum_matching_count = graph.generate_maximum_matching().edge_count()
    return len(bananas) - maximum_matching_count * 2
