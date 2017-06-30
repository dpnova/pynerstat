from twisted.trial import unittest
from minerstat.service import MinerStatService
from minerstat.rig import Rig
from minerstat.utils import Config


class MinerStatServiceTest(unittest.TestCase):

    def setUp(self):
        self.rig = Rig(Config.default())
        self.service = MinerStatService(self.rig)

    def test_init(self):
        MinerStatService(self.rig)

    def test_start_stop(self):
        self.service.startService()
        self.assertTrue(self.service.rig._looper.running)
        self.service.stopService()
        self.assertFalse(self.service.rig._looper.running)


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
