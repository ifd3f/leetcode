import unittest

from distract_the_trainers import is_infinite_cycle, solution, Graph


class TestGraph(unittest.TestCase):
    def test_bipartite(self):
        graph = Graph()
        graph.add_edge_tup((1, 2))
        graph.add_edge_tup((3, 4))
        graph.add_edge_tup((1, 4))

        matching = Graph()
        matching.add_edge_tup((1, 4))

        path = graph.find_augmenting_path(matching)

        self.assertEqual([1, 2, 3, 4], path)


class MyTestCase(unittest.TestCase):
    def test_infinite_cycle(self):
        self.assertTrue(is_infinite_cycle(1, 4))

    def test_case_1(self):
        self.assertEqual(2, solution([1, 1]))

    def test_case_2(self):
        self.assertEqual(0, solution([1, 7, 3, 21, 13, 19]))


if __name__ == '__main__':
    unittest.main()
