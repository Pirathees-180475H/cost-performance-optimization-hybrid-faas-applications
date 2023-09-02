import unittest
from app_register_service import validate_edges
from unittest import TextTestRunner
from unittest import TestCase

class ValidateEdgesTests(unittest.TestCase):
    def test_valid_input(self):
        edges = [(0, 1, 0), (1, 2, 1), (2, 0, 0)]
        functions = ['function1', 'function2', 'function3']
        self.assertIsNone(validate_edges(edges, functions))

    def test_invalid_edge_size_less_than_expected(self):
        edges = [(0, 1)]
        functions = ['function1', 'function2']
        with self.assertRaises(ValueError):
            validate_edges(edges, functions)

    def test_invalid_edge_size_greater_than_expected(self):
        edges = [(0, 1, 0, 1)]
        functions = ['function1', 'function2']
        with self.assertRaises(ValueError):
            validate_edges(edges, functions)

    def test_invalid_node_numbers(self):
        edges = [(0, 3, 0), (1, 2, 1)]
        functions = ['function1', 'function2']
        with self.assertRaises(ValueError):
            validate_edges(edges, functions)

    def test_invalid_probability_values(self):
        edges = [(0, 1, 2), (1, 2, 0.5)]
        functions = ['function1', 'function2', 'function3']
        with self.assertRaises(ValueError):
            validate_edges(edges, functions)

if __name__ == '__main__':
    print('-----------------------------------------------------------------------')
    suite = unittest.TestLoader().loadTestsFromTestCase(ValidateEdgesTests)
    runner = TextTestRunner(verbosity=2)
    runner.run(suite)
