from collections import deque

inf = float('inf')


class Edge:
    def __init__(self, capacity, source, target):
        self.source = source
        self.target = target
        self.capacity = capacity
        self.used = 0

    def is_full(self):
        return self.used == self.capacity


class Node:
    def __init__(self):
        self.neighbors = []

    def send(self, capacity, target):
        """
        Connects this node to the target, with a certain capacity.
        """
        edge = Edge(capacity, self, target)
        self.neighbors.append(edge)
        return edge

    def max_output(self):
        return sum((conn.capacity for conn in self.neighbors))

    def total_used_flow(self):
        return sum((conn.used for conn in self.neighbors))

    def find_open_path(self, sink):
        """
        Performs a BFS for a path that does not have
        """
        # This record is used both as a "visited" set and to aid in back-traversing to build our path.
        node_to_previous_edge = {self: None}

        queue = deque([self])
        while len(queue) > 0:
            node = queue.popleft()

            if node is sink:
                break

            for edge in node.neighbors:
                # Ignore full edges and previously-visited nodes
                if edge.is_full() or edge.target in node_to_previous_edge:
                    continue
                queue.append(edge.target)
                node_to_previous_edge[edge.target] = edge

        # We did not find the sink, so there are no more open paths.
        if sink not in node_to_previous_edge:
            return None

        # Back-traverse to build our path.
        edge = node_to_previous_edge[sink]
        path_to_source = []
        while edge is not None:
            path_to_source.append(edge)
            edge = node_to_previous_edge[edge.source]

        return path_to_source


def build_graph(sources, sinks, network):
    """
    Converts the input matrix and lists into a flow network. If there are multiple sources, creates a super-source
    feeding into all of them, and vice-versa for sinks. Returns the single source and single sink.
    """
    nodes = [Node() for _ in network]

    for source, flows in zip(nodes, network):
        for sink, flow in zip(nodes, flows):
            if flow == 0:
                continue
            source.send(flow, sink)

    # Connect sources to super source
    if len(sources) == 1:
        super_source = nodes[sources[0]]
    else:
        super_source = Node()
        for i_source in sources:
            super_source.send(inf, nodes[i_source])

    # Connect sinks to super sink
    if len(sinks) == 1:
        super_sink = nodes[sinks[0]]
    else:
        super_sink = Node()
        for i_sink in sinks:
            nodes[i_sink].send(inf, super_sink)

    return super_source, super_sink


def augment_edge_path(edges):
    """
    Given a path of edges, augments it by using up the maximum flow through it.
    """
    flow_to_use = min((edge.capacity - edge.used for edge in edges))

    for edge in edges:
        edge.used += flow_to_use


def solution(entrances, exits, path):
    """
    An implementation of the Edmonds-Karp algorithm.
    """
    source, sink = build_graph(entrances, exits, path)

    while True:
        # If there is an available path with unused capacity, then we should augment it.
        path = source.find_open_path(sink)
        if path is None:
            break
        augment_edge_path(path)

    return source.total_used_flow()
