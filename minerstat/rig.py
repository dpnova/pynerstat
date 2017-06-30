from twisted.internet.task import LoopingCall
from twisted.internet import reactor
from minerstat.utils import Config
from twisted.internet.protocol import ProcessProtocol
from twisted.internet.error import ProcessExitedAlready
from twisted.internet.error import ProcessDone, ProcessTerminated
from twisted.python.failure import Failure
from twisted.internet import defer
import subprocess
import os
import asyncio
from typing import Union


class MinerProcessProtocol(ProcessProtocol):

    def __init__(self):
        self.on_ended = defer.Deferred()

    def outReceived(self, data):
        print(data)

    def errReceived(self, data):
        print(data)

    def processEnded(self, status: Failure):
        self.on_ended.callback(status.value)

    def stop_it(self) -> defer.Deferred:
        try:
            self.transport.signalProcess("KILL")
            return self.on_ended
        except ProcessExitedAlready:
            print("Process is already gone.")
            return defer.succeed(None)


class Rig:
    def __init__(
        self,
        config: Config,
        reactor=reactor
    ) -> None:
        self.config = config
        self.reactor = reactor
        self._looper = LoopingCall(self.watchdog)

    def reboot(self):
        """
        Reboot the process.

        NOTE: this depends on the user having passwordless sudo access.
        """
        command = "/usr/bin/sudo /sbin/shutdown -r now"
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
        print(output)

    def start(self) -> None:
        self.header()
        self._looper.start(2)
        self.start_miner()

    async def stop(self) -> None:
        self._looper.stop()
        await self.stop_miner()

    def update_progress_bar(self):
        pass

    def watchdog(self):
        pass

    def header(self):
        print('----------------------- minerstat.com --------------------------')  # noqa
        print('------------------------ Linux Alpha ------------------------')  # noqa
        print('')

    def get_date_time(self):
        pass

    def start_miner(self) -> None:
        self._process_protocol = MinerProcessProtocol()
        path = os.path.join(
            self.config.path,
            "clients",
            self.config.client)
        self.reactor.spawnProcess(
            self._process_protocol,
            os.path.join(path, "start.bash"),
            args=[self.config.client],
            env=os.environ,
            path=path)
        self._process_protocol.on_ended.addCallbacks(
            callback=self.miner_ended,
            errback=self.miner_ended)

    async def stop_miner(self) -> None:
        if self._process_protocol.connected:
            await self._process_protocol.stop_it()

    async def miner_ended(
            self, status: Union[ProcessDone, ProcessTerminated]):
        print(status)
        await asyncio.sleep(1)
        print("restarting miner")
        self.start_miner()
