from __future__ import print_function
import unittest
import sys
import __builtin__
from mock import Mock
sys.modules['RPi'] = Mock()
sys.modules['smbus'] = Mock()

from access import Logger


class LoggerTests(unittest.TestCase):
    def setUp(self):
        self.real_print = __builtin__.print
        self.mock_print = Mock()
        setattr(__builtin__, 'print', self.mock_print)
        self.logger = Logger(None)

    def tearDown(self):
        setattr(__builtin__, 'print', self.real_print)

    def test_debug_mode_is_off_by_default(self):
        self.assertFalse(self.logger.debug_mode)

    def test_without_debug_mode_turned_on_debug_does_nothing(self):
        self.logger.debug('no print')
        self.assertFalse(self.mock_print.called)

    def test_with_debug_mode_turned_on_debug_prints(self):
        self.logger.toggle_debug(None, None)
        self.logger.debug('no print')
        self.assertTrue(self.mock_print.called)

    def test_toggle_debug_turns_on_debug_mode(self):
        self.logger.toggle_debug(None, None)
        self.assertTrue(self.logger.debug_mode)


if __name__ == '__main__':
    unittest.main()
