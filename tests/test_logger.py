import os
import unittest
from werkzeug.security import check_password_hash
from system import shared
from system.Management import Management
from system.files_management.Logger import SimpleTextLogger, InfoTextDecorator, ErrorTextDecorator


class TestLogger(unittest.TestCase):
    def setUp(self):
        self.log_file = 'test_logger.txt'

    def tearDown(self):
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    def test_simple_logger(self):
        test_message = "Test message"
        logger = SimpleTextLogger(test_message)
        self.assertEqual(logger.log(), test_message)

    def test_info_decorator(self):
        test_message = "Test info message"
        simple_logger = SimpleTextLogger(test_message)
        info_logger = InfoTextDecorator(simple_logger)
        self.assertEqual(info_logger.log(), test_message)

    def test_error_decorator(self):
        test_message = "Test error message"
        simple_logger = SimpleTextLogger(test_message)
        error_logger = ErrorTextDecorator(simple_logger)
        self.assertEqual(error_logger.log(), test_message)


if __name__ == '__main__':
    unittest.main()
