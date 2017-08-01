from zope.interface import implementer
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.internet import reactor, defer
from twisted.protocols.basic import LineReceiver
from twisted.plugin import IPlugin
from .base import IMiner
from twisted.logger import Logger
from typing import Awaitable


class SGLineReceiver(LineReceiver):

    log = Logger()

    delimiter = b"\0"

    def __init__(self) -> None:
        self._response_d = defer.Deferred()

    def make_request(self, request) -> Awaitable:
        self.transport.write(request)
        self.transport.write(b"\n")
        return self._response_d


@implementer(IPlugin, IMiner)
class SGMiner:
    name = "sgminer-gm"
    folder_name = "sgminer-gm"
    db = "sgg_conf"
    config_name = "sgminer.conf"
    coin = ""
    command = "SWITCHTOSGGM"
    execute = "sgminer-gm"
    config_template = "{0}"

    async def fetch_logs(self) -> bytes:
        """Use a connection to the socket to get the logs."""
        host = "127.0.0.1"
        port = 4028

        request = "summary"

        point = TCP4ClientEndpoint(reactor, host, port)
        try:
            connected_p = await connectProtocol(
                point, SGLineReceiver())  # type: SGLineReceiver
            response = await connected_p.make_request(request)
        except Exception as e:
            print("couldn't connect. {}".format(e))
            return b""
        else:
            objs = response.split(r"|")
            for obj in objs:
                if obj:
                    items = obj.split(",")
                    item = items[0]
                    id = item.split("=")
            return b" "
