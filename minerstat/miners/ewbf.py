from datetime import datetime
from zope.interface import implementer
from twisted.plugin import IPlugin
from .base import IMiner
from twisted.internet import reactor, protocol, defer
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
import pytz
import json


class EWBFProtocol(protocol.Protocol):
    def make_request(self, request):
        self.transport.write(json.dumps(request))
        self._response_d = defer.Deferred()
        return self._response_d

    def dataReceived(self, data: bytes):
        if data and data[-1] == b'}':
            try:
                val = json.loads(data)
            except:
                print("not valid")
                raise
            else:
                self._response_d.callback(val)
        return


@implementer(IPlugin, IMiner)
class EWBFZecMiner:
    name = "ewbf-zec"
    folder_name = "ewbf-zec"
    db = "ezec_conf"
    config_name = "start.bash"
    coin = ""
    command = "SWITCHTOEZEC"
    execute = "start.bash"

    async def fetch_log(self) -> bytes:
        """Use a connection to the socket to get the logs."""
        host = "127.0.0.1"
        port = 42000
        dt = datetime.now(pytz.timezone("Europe/Amsterdam"))
        request = {"id": 1, "method": "getstat"}

        point = TCP4ClientEndpoint(reactor, host, port)
        connected_p = await connectProtocol(
            point, EWBFProtocol())  # type: EWBFProtocol
        response = await connected_p.sendRequest(json.dumps(request))
        rl = []
        t = 0  # type: int
        power = speed = accept = reject = 0
        for idx, (gpu_id, data) in enumerate(response['result'].items()):
            rl.append("GPU_{0}_SPEED: {1} H/s".format(
                gpu_id, data['speed_sps']))
            rl.append("GPU_{0}_POWER: {1}".format(
                gpu_id, data['gpu_power_usage']))
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
        rl.append("START_TIME: {0}".format(t))
        rl.append("CURRENT_TIME: {0}".format(dt.timestamp()))
        rl.append("UPTIME: {0}".format(dt.timestamp() - t))
        return ";".join(rl).encode('utf-8')
