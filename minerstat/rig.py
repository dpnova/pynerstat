from twisted.internet.task import LoopingCall
from twisted.internet import reactor
from minerstat.utils import Config
from minerstat.remote import MinerStatRemoteProtocol
from twisted.internet.protocol import ProcessProtocol
from twisted.internet.error import ProcessExitedAlready
from twisted.internet.error import ProcessDone, ProcessTerminated
from twisted.python.failure import Failure
from twisted.internet import defer, task
import subprocess
import os
from typing import Union
from twisted.logger import Logger
import asyncio
from twisted.plugin import getPlugins
from minerstat.miners.base import IMiner, MinerUtils


class MinerProcessProtocol(ProcessProtocol):

    log = Logger()

    def __init__(self):
        self.on_ended = defer.Deferred()

    def outReceived(self, data):
        print(data)

    def errReceived(self, data):
        print(data)

    def processExited(self, status: Failure):
        self.log.debug(
            "miner process has exited with status: {status}", status=status)

    def processEnded(self, status: Failure):
        self.log.debug(
            "miner process has ended with status: {status}", status=status)
        self.on_ended.callback(status.value)

    def stop_it(self) -> defer.Deferred:
        self.log.debug("Stopping the miner.")
        try:
            self.transport.signalProcess("KILL")
            return self.on_ended
        except ProcessExitedAlready:
            self.log.info("Miner process is already gone.")
            return defer.succeed(None)


class Rig:

    log = Logger()

    def __init__(
        self,
        config: Config,
        remote: MinerStatRemoteProtocol,
        reactor=reactor
    ) -> None:
        self.config = config
        self.remote = remote
        self.reactor = reactor
        self._looper = LoopingCall(self.mainloop)
        self._coin_lock = asyncio.Lock()
        self._current_coin = None  # Type: IMiner

    def reboot(self) -> None:
        """
        Reboot the service.

        NOTE: this depends on the user having passwordless sudo access.
        """
        command = "/usr/bin/sudo /sbin/shutdown -r now"
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
        print(output)

    async def start(self) -> None:
        self.header()
        await self.load_configured_miner()
        self.start_miner()
        self._looper.start(20)

    async def stop(self) -> None:
        self._looper.stop()
        await self.stop_miner()

    async def load_configured_miner(self) -> IMiner:
        miner_coins = getPlugins(IMiner)  # Type: List[IMiner]
        for coin in miner_coins:
            if coin.name == self.config.client:
                await self.remote.dlconf(coin)
        else:
            raise RuntimeError("No miner configured in global config.")

    def watchdog(self):
        pass

    def mainloop(self) -> None:
        data = self.collect_miner_data()
        self.send_logs_to_server(data)
        self.check_algorithms()
        self.check_remote_commands()
        self.watchdog()

    def check_algorithms(self) -> None:
        """call to self.remote.check_algo"""

    async def setup_miner(self, coin: IMiner) -> None:
        with (await self._coin_lock):
            await self.stop_miner()
            self._current_coin = coin
            self.start_miner()

    async def check_remote_commands(self) -> None:
        """call to self.dispatch_remote"""
        command = await self.remote.fetch_remote_command()
        if command and command.coin:
            await self.setup_miner(command.coin)

    def collect_miner_data(self) -> str:
        """hit the subprocess protocol to get buffers"""

    def send_logs_to_server(self, data: str) -> None:
        """use self.remote.send_logs"""

    def header(self):
        self.log.info('----------------------- minerstat.com --------------------------')  # noqa
        self.log.info('------------------------ Linux Alpha ------------------------')  # noqa

    def start_miner(self) -> None:
        self._process_protocol = MinerProcessProtocol()
        util = MinerUtils(coin, self.config)
        path = util.miner_path()
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

    @defer.inlineCallbacks
    def miner_ended(
            self, status: Union[ProcessDone, ProcessTerminated]):
        self.log.info("Got satus from ending miner. {status}", status=status)
        yield task.deferLater(self.reactor, 1, self.start_miner)
        self.log.info("Started miner: {miner}", miner=self.config.client)
