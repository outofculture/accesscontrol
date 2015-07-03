from __future__ import print_function
from datetime import datetime
import unittest
import sys
import __builtin__
from datetime import timedelta
from freezegun.api import freeze_time
from mock import Mock, patch

mock_rpi = Mock()
sys.modules['RPi'] = mock_rpi
sys.modules['smbus'] = Mock()

from access import Logger, Door, Output


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

    def test_open_door_does_not_change_unlocked_on_its_first_call(self):
        self.assertFalse(self.door.unlocked)
        self.door.open_door({'name': 'test user'})
        self.assertFalse(self.door.unlocked)

    def test_open_door_sets_unlocked_to_true_after_the_third_call(self):
        self.assertFalse(self.door.unlocked)
        self.door.open_door({'name': 'test user'})
        with freeze_time(datetime.now() + timedelta(microseconds=35)):
            self.door.open_door({'name': 'test user'})
        with freeze_time(datetime.now() + timedelta(microseconds=70)):
            self.door.open_door({'name': 'test user'})
            self.assertTrue(self.door.unlocked)

    @unittest.skip('todo')
    def test_repeat_calls_to_open_door_with_different_users_will_not_count_toward_unlocking(self, mock_output):
        self.fail()


class OutputTests(unittest.TestCase):
    def setUp(self):
        self.unlock_value = 1
        self.lock_value = self.unlock_value ^ 1
        mock_rpi.reset_mock()
        self.output = Output(1, self.unlock_value, 0)

    def test_initialization_sends_deactivation_signal(self):
        mock_rpi.GPIO.output.assert_called_once_with(self.output.address, self.lock_value)


if __name__ == '__main__':
    unittest.main()
