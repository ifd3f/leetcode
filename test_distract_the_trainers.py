import unittest
from copy import deepcopy

from distract_the_trainers import is_infinite_cycle, solution, Graph, augment


def generate_simple_blossom_graph():
    graph = Graph()
    graph.add_edge_tup((1, 2))
    graph.add_edge_tup((2, 3))
    graph.add_edge_tup((2, 6))
    graph.add_edge_tup((3, 4))
    graph.add_edge_tup((4, 5))
    graph.add_edge_tup((5, 6))
    graph.add_edge_tup((5, 7))
    graph.add_edge_tup((7, 8))
    graph.add_edge_tup((8, 9))
    return graph


class TestGraph(unittest.TestCase):
    def test_snake(self):
        graph = Graph()
        graph.add_edge_tup((1, 2))
        graph.add_edge_tup((3, 4))
        graph.add_edge_tup((3, 2))

        matching = Graph()
        matching.add_edge_tup((2, 3))

        path = graph.find_augmenting_path(matching)

        self.assertIn(path, [[1, 2, 3, 4], [4, 3, 2, 1]])

    def test_deepcopy(self):
        graph = Graph()
        graph.add_edge_tup((1, 2))
        graph.add_edge_tup((3, 4))
        graph.add_edge_tup((3, 2))

        graph_copy = deepcopy(graph)
        graph_copy.add_edge_tup((5, 2))

        self.assertIn((2, 5), graph_copy.edges())
        self.assertNotIn((2, 5), graph.edges())

    def test_blossom_1(self):
        graph = Graph()
        graph.add_edge_tup((1, 4))
        graph.add_edge_tup((2, 4))
        graph.add_edge_tup((3, 5))
        graph.add_edge_tup((4, 5))

        matching = graph.maximum_matching()

        self.assertEqual(2, matching.edge_count())

    def test_blossom_2(self):
        graph = Graph()
        graph.add_edge_tup((1, 2))
        graph.add_edge_tup((1, 3))
        graph.add_edge_tup((2, 3))
        graph.add_edge_tup((2, 4))
        graph.add_edge_tup((3, 5))
        graph.add_edge_tup((4, 5))
        graph.add_edge_tup((4, 6))

        matching = graph.maximum_matching()

        self.assertEqual(3, matching.edge_count())

    def test_blossom_3(self):
        graph = Graph()
        graph.add_edge_tup((1, 2))
        graph.add_edge_tup((1, 12))
        graph.add_edge_tup((2, 3))
        graph.add_edge_tup((3, 4))
        graph.add_edge_tup((3, 7))
        graph.add_edge_tup((3, 10))
        graph.add_edge_tup((4, 5))
        graph.add_edge_tup((5, 6))
        graph.add_edge_tup((5, 8))
        graph.add_edge_tup((6, 9))
        graph.add_edge_tup((7, 10))
        graph.add_edge_tup((9, 11))
        graph.add_edge_tup((11, 12))

        matching = graph.maximum_matching()

        self.assertEqual(5, matching.edge_count())

    def test_icp_ideal(self):
        graph = generate_simple_blossom_graph()
        path = [0, 1, 2, 7]
        cycle = [2, 3, 4, 5, 6]

        intra_cycle = graph.get_intra_cycle_path(path, cycle, 2)

        self.assertEqual([2, 6, 5], intra_cycle)

    def test_icp_cycle_rotation(self):
        graph = generate_simple_blossom_graph()
        path = [0, 1, 2, 7]
        cycle = [5, 6, 2, 3, 4]

        intra_cycle = graph.get_intra_cycle_path(path, cycle, 2)

        self.assertEqual([2, 6, 5], intra_cycle)

    def test_icp_contracted_as_root_1(self):
        graph = generate_simple_blossom_graph()
        path = [2, 7, 8, 9]
        cycle = [2, 3, 4, 5, 6]

        intra_cycle = graph.get_intra_cycle_path(path, cycle, 0)

        self.assertEqual([2, 6, 5], intra_cycle)

    def test_icp_contracted_as_root_2(self):
        graph = generate_simple_blossom_graph()
        path = [2, 7, 8, 9]
        cycle = [3, 4, 5, 6, 2]

        intra_cycle = graph.get_intra_cycle_path(path, cycle, 0)

        self.assertEqual([3, 4, 5], intra_cycle)

    def test_count_bipartite_1(self):
        graph = Graph()
        graph.add_edge_tup((1, 2))
        graph.add_edge_tup((3, 4))
        graph.add_edge_tup((1, 4))
        graph.add_edge_tup((5, 2))

        matching = graph.maximum_matching()

        self.assertEqual(2, matching.edge_count())

    def test_count_bipartite_2(self):
        graph = Graph()
        graph.add_edge_tup((1, 2))
        graph.add_edge_tup((1, 4))
        graph.add_edge_tup((3, 4))
        graph.add_edge_tup((3, 6))
        graph.add_edge_tup((5, 2))
        graph.add_edge_tup((7, 2))
        graph.add_edge_tup((7, 6))

        matching = graph.maximum_matching()

        self.assertEqual(3, matching.edge_count())

    def test_count_bipartite_3(self):
        graph = Graph()
        graph.add_edge_tup((1, 4))
        graph.add_edge_tup((1, 6))
        graph.add_edge_tup((5, 2))
        graph.add_edge_tup((5, 8))
        graph.add_edge_tup((7, 6))
        graph.add_edge_tup((9, 6))
        graph.add_edge_tup((9, 8))
        graph.add_edge_tup((11, 12))

        matching = graph.maximum_matching()

        self.assertEqual(5, matching.edge_count())

    def test_augment(self):
        path = [1, 2, 3, 4]

        matching = Graph()
        matching.add_edge_tup((2, 3))

        augment(path, matching)

        self.assertIn((1, 2), matching.edges())
        self.assertNotIn((2, 3), matching.edges())
        self.assertIn((3, 4), matching.edges())
        self.assertNotIn((1, 3), matching.edges())


class TestSolution(unittest.TestCase):
    def test_infinite_cycle(self):
        self.assertTrue(is_infinite_cycle(1, 4))

    def test_case_1(self):
        self.assertEqual(2, solution([1, 1]))

    def test_case_2(self):
        self.assertEqual(0, solution([1, 7, 3, 21, 13, 19]))


if __name__ == '__main__':
    unittest.main()
