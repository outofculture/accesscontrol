from __future__ import print_function
from datetime import datetime
import unittest
import sys
import __builtin__
from datetime import timedelta
from freezegun.api import freeze_time
from mock import Mock, patch

sys.modules['RPi'] = Mock()
sys.modules['smbus'] = Mock()

from access import Logger, Door


class LoggerTests(unittest.TestCase):
    def setUp(self):
        self.real_print = __builtin__.print
        self.mock_print = Mock()
        setattr(__builtin__, 'print', self.mock_print)
        self.logger = Logger({})

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


@patch('access.Output', autospec=True)
class DoorTests(unittest.TestCase):
    def setUp(self):
        self.mock_reader = Mock()
        config = {
            'name': '',
            'latch_gpio': 1,
            'unlock_value': 1,
            'open_delay': 0,
        }
        self.door = Door(config, self.mock_reader)

    def test_open_door_does_not_change_unlocked_on_its_first_call(self, mock_output):
        self.assertFalse(self.door.unlocked)
        self.door.open_door({'name': 'test user'})
        self.assertFalse(self.door.unlocked)

    def test_open_door_sets_unlocked_to_true_after_the_third_call(self, mock_output):
        self.assertFalse(self.door.unlocked)
        self.door.open_door({'name': 'test user'})
        with freeze_time(datetime.now() + timedelta(microseconds=35)):
            self.door.open_door({'name': 'test user'})
        with freeze_time(datetime.now() + timedelta(microseconds=70)):
            self.door.open_door({'name': 'test user'})
            self.assertTrue(self.door.unlocked)


if __name__ == '__main__':
    unittest.main()
