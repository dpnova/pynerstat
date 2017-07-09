from datetime import datetime
from zope.interface import implementer
from twisted.plugin import IPlugin
from .base import IMiner
from twisted.internet import reactor, protocol, defer
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
import pytz
import json
from typing import Awaitable
from twisted.python import failure


class EWBFProtocol(protocol.Protocol):

    def __init__(self) -> None:
        self._response_d = defer.Deferred()

    def make_request(self, request) -> Awaitable:
        data = json.dumps(request).encode("utf-8")
        self.transport.write(data)
        self.transport.write(b"\n")
        return self._response_d

    def dataReceived(self, data: bytes) -> None:
        try:
            print(data)
            val = json.loads(data.decode("utf-8"))
        except:
            print("not valid")
            raise
        else:
            d, self._response_d = self._response_d, None
            d.callback(val)
        return

    def connectionMade(self) -> None:
        print("CONNECTION WAS MADE")

    def connectionLost(self, reason: failure.Failure) -> None:
        if self._response_d:
            print("CONNECTION DEAD")
            self._response_d.errback(reason)


@implementer(IPlugin, IMiner)
class EWBFZecMiner:
    name = "ewbf-zec"
    folder_name = "ewbf-zec"
    db = "ezec_conf"
    config_name = "start.bash"
    coin = ""
    command = "SWITCHTOEZEC"
    execute = "start.bash"
    config_template = "#!/usr/bin/env sh\nexec {0}"

    async def fetch_logs(self) -> bytes:
        """Use a connection to the socket to get the logs."""
        host = "127.0.0.1"
        port = 42000
        dt = datetime.now(pytz.timezone("Europe/Amsterdam"))
        request = {"id": 1, "method": "getstat"}

        point = TCP4ClientEndpoint(reactor, host, port)
        try:
            connected_p = await connectProtocol(
                point, EWBFProtocol())  # type: EWBFProtocol
            response = await connected_p.make_request(request)
        except Exception as e:
            print("couldn't connect. {}".format(e))
            return b""
        else:
            rl = []
            t = 0  # type: int
            power = speed = accept = reject = 0
            for idx, data in enumerate(response['result']):
                rl.append("GPU{0}_SPEED: {1} H/s".format(
                    idx, data['speed_sps']))
                rl.append("GPU{0}_POWER: {1}".format(
                    idx, data['gpu_power_usage']))
                t = data['start_time']
                power += data['gpu_power_usage']
                speed += data['speed_sps']
                accept += data['accepted_shares']
                reject += data['rejected_shares']

            rl.append("Power: {0}".format(power))
            rl.append("Total speed: {0} Sol/s".format(speed))
            rl.append("Accepted share: {0}".format(accept))
            rl.append("Rejected share: {0}".format(reject))
            rl.append("Total GPUs: {0}".format(len(response['result'])))
            rl.append("START_TIME: {0}".format(int(t)))
            rl.append("CURRENT_TIME: {0}".format(int(dt.timestamp())))
            rl.append("UPTIME: {0}".format(int(dt.timestamp() - t)))
            return ";".join(rl).encode('utf-8') + b";"
