from twisted.trial import unittest
from minerstat.service import MinerStatService


class MinerStatServiceTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_init(self):
        MinerStatService()

    def test_start(self):
        pass

    def test_stop(self):
        pass

class MinerStatRemoteProtocolTest(unittest.TestCase):

    def test_algoinfo(self):
        pass

    def test_dlconf(self):
        pass

    def test_send_log(self):
        pass

    def algo_check(self):
        pass

    def test_dispatch_remote_command(self):
        pass

    def test_poll_remote(self):
        pass
