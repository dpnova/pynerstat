from twisted.trial import unittest
from minerstat.service import MinerStatService
from minerstat.rig import Rig
from minerstat.utils import Config
from twisted.internet import task, defer
from mock import Mock


class MinerStatServiceTest(unittest.TestCase):

    def setUp(self):
        self.clock = task.Clock()
        self.clock.spawnProcess = Mock()
        self.rig = Rig(Config.default(), reactor=self.clock)
        self.service = MinerStatService(self.rig)

    def test_init(self):
        MinerStatService(self.rig)

    @defer.inlineCallbacks
    def test_start_stop(self):
        self.service.startService()
        self.assertTrue(self.service.rig._looper.running)
        yield defer.ensureDeferred(self.service.stopService())
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
