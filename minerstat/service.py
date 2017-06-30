from twisted.application.service import Service
from zope.interface import implementer
from twisted.internet.interfaces import IProtocol
from twisted.internet.protocol import ProcessProtocol
from minerstat.rig import Rig


@implementer(IProtocol)
class MinerStateRemoteProtocol:

    def algoinfo(self):
        pass

    def dlconf(self):
        pass

    def send_log(self):
        pass

    def algo_check(self):
        pass

    def dispatch_remote_command(self):
        pass

    def poll_remote(self):
        pass


class MinerProcessProtocol(ProcessProtocol):

    pass


class MinerStatService(Service):
    def __init__(self, rig: Rig) -> None:
        self.rig = rig

    def startService(self) -> None:
        self.rig.start()

    async def stopService(self) -> None:
        await self.rig.stop()
