import unittest
import os
from app_register_service import functions_name_collector
from unittest import TextTestRunner
from unittest import TestCase

class FunctionsNameCollectorTests(unittest.TestCase):

    def setUp(self):
        self.folder_with_functions = "C:/Users/PTS/Desktop/FYP/functions/App6"
        self.folder_without_functions = "C:/Users/PTS/Desktop/FYP/functions/App6/x"
        self.folder_with_non_py_files = "C:/Users/PTS/Desktop/FYP/functions/App6/y"
        self.empty_folder = "C:/Users/PTS/Desktop/FYP/functions/App6/z"
        self.invalid_folder = "path/to/invalid_folder"

    def test_collect_functions_from_folder_with_functions(self):
        expected_functions = ["f1", "f2", "f3","f4","f5","f6"]
        result = functions_name_collector(self.folder_with_functions)
        self.assertEqual(result, expected_functions)

    def test_collect_functions_from_folder_without_functions(self):
        expected_functions = []
        result = functions_name_collector(self.folder_without_functions)
        self.assertEqual(result, expected_functions)

    def test_collect_functions_from_folder_with_non_py_files(self):
        expected_functions = []
        result = functions_name_collector(self.folder_with_non_py_files)
        self.assertEqual(result, expected_functions)

    def test_collect_functions_from_empty_folder(self):
        expected_functions = []
        result = functions_name_collector(self.empty_folder)
        self.assertEqual(result, expected_functions)

    def test_collect_functions_from_invalid_folder(self):
        with self.assertRaises(Exception):
            functions_name_collector(self.invalid_folder)

if __name__ == '__main__':
    print('-----------------------------------------------------------------------')

    suite = unittest.TestLoader().loadTestsFromTestCase(FunctionsNameCollectorTests)
    runner = TextTestRunner(verbosity=2)
    runner.run(suite)
