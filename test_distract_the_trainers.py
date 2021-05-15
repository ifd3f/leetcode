import unittest

from distract_the_trainers import is_infinite_cycle, solution, Graph, augment


class TestGraph(unittest.TestCase):
    def test_snake_4(self):
        graph = Graph()
        graph.add_edge_tup((1, 2))
        graph.add_edge_tup((3, 4))
        graph.add_edge_tup((3, 2))

        matching = Graph()
        matching.add_edge_tup((2, 3))

        path = graph.find_augmenting_path(matching)

        self.assertIn(path, [[1, 2, 3, 4], [4, 3, 2, 1]])

    def test_count_bipartite_1(self):
        graph = Graph()
        graph.add_edge_tup((1, 2))
        graph.add_edge_tup((3, 4))
        graph.add_edge_tup((1, 4))
        graph.add_edge_tup((5, 2))

        count = graph.count_maximum_matching()

        self.assertEqual(count, 2)

    def test_count_bipartite_2(self):
        graph = Graph()
        graph.add_edge_tup((1, 2))
        graph.add_edge_tup((1, 4))
        graph.add_edge_tup((3, 4))
        graph.add_edge_tup((3, 6))
        graph.add_edge_tup((5, 2))
        graph.add_edge_tup((7, 2))
        graph.add_edge_tup((7, 6))

        count = graph.count_maximum_matching()

        self.assertEqual(count, 4)

    def test_augment(self):
        path = [1, 2, 3, 4]

        matching = Graph()
        matching.add_edge_tup((2, 3))

        augment(path, matching)

        self.assertIn((1, 2), matching.edges())
        self.assertNotIn((2, 3), matching.edges())
        self.assertIn((3, 4), matching.edges())
        self.assertNotIn((1, 3), matching.edges())


class MyTestCase(unittest.TestCase):
    def test_infinite_cycle(self):
        self.assertTrue(is_infinite_cycle(1, 4))

    def test_case_1(self):
        self.assertEqual(2, solution([1, 1]))

    def test_case_2(self):
        self.assertEqual(0, solution([1, 7, 3, 21, 13, 19]))


if __name__ == '__main__':
    unittest.main()
