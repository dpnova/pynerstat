from zope.interface import implementer
from twisted.plugin import IPlugin
from .base import IMiner
import treq
from twisted.logger import Logger


@implementer(IPlugin, IMiner)
class EthClaymoreMiner:

    log = Logger()

    name = "claymore-eth"
    folder_name = "claymore-eth"
    db = "eth_conf"
    config_name = "config.txt"
    coin = "eth"
    command = "SWITCHTOETH"
    execute = "start.bash"
    config_template = "{0}"

    async def fetch_logs(self) -> bytes:
        res = await treq.get("http://localhost:3333").addErrback(self.log.info)
        if res:
            text = await res.content()
            return text
        return bytes()


@implementer(IPlugin, IMiner)
class AlgoClaymoreMiner(EthClaymoreMiner):
    name = "algo"
    coin = ""


@implementer(IPlugin, IMiner)
class DualClaymoreMiner(AlgoClaymoreMiner):
    name = "algo"
    db = "null"


@implementer(IPlugin, IMiner)
class EtcClaymoreMiner(EthClaymoreMiner):
    name = "claymore-etc"
    coin = "etc"
    command = "SWITCHTOETC"


@implementer(IPlugin, IMiner)
class ExpClaymoreMiner(EthClaymoreMiner):
    name = "claymore-exp"
    coin = "exp"
    command = "SWITCHTOEXP"


@implementer(IPlugin, IMiner)
class MusicClaymoreMiner(EthClaymoreMiner):
    name = "claymore-music"
    coin = "music"
    command = "SWITCHTOMUSIC"


@implementer(IPlugin, IMiner)
class UbqClaymoreMiner(EthClaymoreMiner):
    name = "claymore-ubq"
    coin = "ubq"
    command = "SWITCHTOUBQ"


@implementer(IPlugin, IMiner)
class ZecClaymoreMiner:

    log = Logger()

    name = "claymore-zec"
    folder_name = "claymore-zec"
    db = "zec_conf"
    config_name = "config.txt"
    coin = ""
    command = "SWITCHTOZEC"
    execute = "start.bash"
    config_template = "{0}"

    async def fetch_logs(self) -> bytes:
        res = await treq.get("http://localhost:3333").addErrback(self.log.info)
        if res:
            text = await res.content()
            return text
        return bytes()
