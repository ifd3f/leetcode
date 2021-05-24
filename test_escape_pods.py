import unittest

from escape_pods import solution, build_graph, Node


class GraphTests(unittest.TestCase):
    def test_build_graph(self):
        source, sink = build_graph([0], [3], [
            [0, 7, 0, 0],
            [0, 0, 6, 0],
            [0, 0, 0, 8],
            [9, 0, 0, 0]
        ])

        self.assertEqual(1, len(source.neighbors))
        source_edge = source.neighbors[0]
        self.assertEqual(7, source_edge.capacity)

    def test_find_unused_path_1(self):
        source = Node()
        n0 = Node()
        sink = Node()
        e1 = source.send(4, n0)
        e2 = n0.send(4, sink)

        path = source.find_open_path(sink)

        self.assertEqual([e2, e1], path)

    def test_find_unused_path_2(self):
        source = Node()
        n0 = Node()
        n1 = Node()
        n2 = Node()
        sink = Node()
        source.send(1, n1)
        n1.send(1, n2)
        n2.send(1, sink)
        e1 = source.send(4, n0)
        e2 = n0.send(4, sink)

        path = source.find_open_path(sink)

        self.assertEqual([e2, e1], path)

    def test_find_unused_path_with_full_edge(self):
        source = Node()
        n0 = Node()
        sink = Node()
        e1 = source.send(4, n0)
        e2 = n0.send(4, sink)
        e2.used = 4

        path = source.find_open_path(sink)

        self.assertIsNone(path)


class EscapePodTests(unittest.TestCase):
    def test_solution_provided_1(self):
        result = solution(
            [0], [3], [
                [0, 7, 0, 0],
                [0, 0, 6, 0],
                [0, 0, 0, 8],
                [9, 0, 0, 0]
            ])
        self.assertEqual(6, result)

    def test_solution_provided_2(self):
        result = solution(
            [0, 1], [4, 5],
            [[0, 0, 4, 6, 0, 0],
             [0, 0, 5, 2, 0, 0],
             [0, 0, 0, 0, 4, 4],
             [0, 0, 0, 0, 6, 6],
             [0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0]]
        )
        self.assertEqual(16, result)


if __name__ == '__main__':
    unittest.main()
