# Standard library imports
from typing import override
import unittest

# Local application imports
import logger.bcolors
import logger


class log_recorder(logger.obj_type):
    def __init__(
        self,
        rcc_logs: logger.filter.filter_type_bin,
        player_logs: logger.filter.filter_type_bin,
        web_logs: logger.filter.filter_type_web,
        bcolors: logger.bcolors.bcolors,
        other_logs: bool = True,
    ) -> None:
        self.log_records: list[str] = []
        super().__init__(
            rcc_logs, player_logs, web_logs, other_logs, bcolors,
            action=lambda m: self.log_records.append(m)
        )


class TestLogs(unittest.TestCase):
    def test_print_message(self):
        '''
        Tests that any message prints at all.
        '''
        recorder = log_recorder(
            rcc_logs=logger.filter.FILTER_BIN_LOUD,
            player_logs=logger.filter.FILTER_BIN_LOUD,
            web_logs=logger.filter.FILTER_WEB_LOUD,
            bcolors=logger.bcolors.BCOLORS_INVISIBLE,
            other_logs=True,
        )
        recorder.log(
            text='67',
            context=logger.log_context.PYTHON_SETUP,
        )
        self.assertIn('67', recorder.log_records, 'No message found')

    def test_print_url(self):
        '''
        Tests that webserver URLs can be printed.
        '''
        recorder = log_recorder(
            rcc_logs=logger.filter.FILTER_BIN_LOUD,
            player_logs=logger.filter.FILTER_BIN_LOUD,
            web_logs=logger.filter.FILTER_WEB_LOUD,
            bcolors=logger.bcolors.BCOLORS_INVISIBLE,
            other_logs=True,
        )
        recorder.log(
            text='67',
            context=logger.log_context.PYTHON_SETUP,
        )
        self.assertIn('67', recorder.log_records, 'No message found')
