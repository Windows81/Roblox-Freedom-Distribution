# Standard library imports
import time
from typing import override
import unittest
import random

# Local application imports
from util import resource
import game_config
import routines
import logger

from routines import (
    rcc,
    web,
)

from . import test_logger


class TestServer(unittest.TestCase):
    @override
    @classmethod
    def setUpClass(cls):
        cls.base_dir = resource.retr_full_path(resource.dir_type.WORKING_DIR)
        cls.game_config = game_config.obj_type(
            data_dict={
                'server_core': {'place_file': {'rbxl_uri': 'https://github.com/Perthys/chalk/raw/main/ExampleGame.rbxl'}}
            },
            base_dir=cls.base_dir,
        )
        cls.random_port = random.randint(49152, 65535)

        cls.logger = test_logger.log_recorder(
            rcc_logs=logger.filter.FILTER_BIN_LOUD,
            player_logs=logger.filter.FILTER_BIN_LOUD,
            web_logs=logger.filter.FILTER_WEB_LOUD,
            bcolors=logger.bc.BCOLORS_INVISIBLE,
            other_logs=True,
        )
        cls.routine = routines.routine(
            web.obj_type(
                web_port=cls.random_port,
                logger=cls.logger,
                game_config=cls.game_config,
                server_mode=web.SERVER_MODE_TYPE.RCC,
                is_ipv6=False,
                is_ssl=True,
            ),
            rcc.obj_type(
                rcc_port=cls.random_port,
                web_port=cls.random_port,
                logger=cls.logger,
                game_config=cls.game_config,
            ),
        )
        time.sleep(30)
        cls.all_log_text = '\n'.join(cls.logger.log_records)

    @override
    @classmethod
    def tearDownClass(cls):
        cls.routine.kill()

    def test_servers_started(self) -> None:
        '''
        Tests whether RFD correclty signals that the port is opened for TCP and UDP.
        '''
        self.assertIn(f'UDP {self.random_port}', self.all_log_text)
        self.assertIn(f'TCP {self.random_port}', self.all_log_text)

    def test_data_is_transferable(self) -> None:
        self.assertIn(
            f':{self.random_port}/rfd/data-transfer',
            self.all_log_text,
        )
