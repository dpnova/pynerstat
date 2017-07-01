from twisted.trial import unittest
from minerstat.service import MinerStatService
from minerstat.rig import Rig
from minerstat.remote import MinerStatRemoteProtocol
from minerstat.utils import Config
from twisted.internet import task, defer
from mock import Mock, create_autospec
import treq


class MinerStatServiceTest(unittest.TestCase):

    def setUp(self):
        self.clock = task.Clock()
        self.clock.spawnProcess = Mock()
        treq_mock = create_autospec(treq)
        self.config = Config.default()
        self.remote = MinerStatRemoteProtocol(self.config, treq_mock)
        self.rig = Rig(self.config, remote=self.remote, reactor=self.clock)
        self.service = MinerStatService(self.rig)

    def test_init(self):
        MinerStatService(self.rig)

    @defer.inlineCallbacks
    def test_start_stop(self):
        yield self.service.startService()
        self.assertTrue(self.service.rig._looper.running)
        yield self.service.stopService()
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
