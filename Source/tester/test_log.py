import unittest
import logger


class TestLog(unittest.TestCase):
    def test_message_rcc_match(self) -> None:
        '''
        Tests if the function correctly identifies a match between the message and RCC.
        '''
        message = logger.get_message(
            "1734559470.58408,7884,19,GameServer,1818,13058,https://localhost:2005/.127.0.0.1,Test,https://localhost:2005,unknown,Test [DFLog::NetworkAudit] Curl Close: ::52f0:1810:f40c:e23f|2005 after 0.020003",
            context=logger.log_context.RCC_SERVER,
        )
        self.assertIsNotNone(message)
