import unittest

from escape_pods import solution, build_graph


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
