from twisted.application.service import Service
from minerstat.rig import Rig
from twisted.internet import defer


class MinerStatService(Service):
    def __init__(self, rig: Rig) -> None:
        self.rig = rig

    def startService(self) -> None:
        self.rig.start()

    def stopService(self) -> None:
        return defer.ensureDeferred(self.rig.stop())
