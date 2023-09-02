import unittest
from app_register_service import validate_functions, functions_name_collector
from unittest import TextTestRunner
from unittest import TestCase
import time

class CreateApplicationTests(unittest.TestCase):

    def test_valid_input(self):
        functions = [{'functionName': 'function1','functionShortName': 'f1','functionType': 'CPU'},
            {'functionName': 'function2','functionShortName': 'f2','functionType': 'Network'},
            {'functionName': 'function3','functionShortName': 'f3','functionType': 'Disk'},
            {'functionName': 'function4','functionShortName': 'f4','functionType': 'Disk'},
            {'functionName': 'function5','functionShortName': 'f5','functionType': 'Disk'},
            {'functionName': 'function6','functionShortName': 'f6','functionType': 'Disk'}
            ]
        functionCount = 6
        folder_location = "C:/Users/PTS/Desktop/FYP/functions/App6"
        self.assertIsNone(validate_functions(functions, functionCount, folder_location))

    def test_invalid_user(self):
        functions = [{'functionName': 'function1','functionShortName': 'func1','functionType': 'CPU'},
            {'functionName': 'function2','functionShortName': 'func2','functionType': 'Network'}]
        functionCount = 3
        folder_location = "C:/Users/PTS/Desktop/FYP/functions/App6"
        with self.assertRaises(ValueError):
            validate_functions(functions, functionCount, folder_location)

    def test_missing_application_name(self):
        time.sleep(10)
        functions = [{'functionShortName': 'func1','functionType': 'CPU'},
            {'functionName': 'function2','functionShortName': 'func2','functionType': 'Network'}
        ]
        functionCount = 6
        folder_location = "C:/Users/PTS/Desktop/FYP/functions/App6"
        with self.assertRaises(ValueError):
            validate_functions(functions, functionCount, folder_location)

if __name__ == '__main__':
    print('-----------------------------------------------------------------------')
    suite = unittest.TestLoader().loadTestsFromTestCase(CreateApplicationTests)
    runner = TextTestRunner(verbosity=2)
    runner.run(suite)
