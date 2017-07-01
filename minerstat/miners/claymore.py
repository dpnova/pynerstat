from zope.interface import implementer
from twisted.plugin import IPlugin
from .base import IMiner


@implementer(IPlugin, IMiner)
class EthClaymoreMiner:
    name = "claymore-eth"
    db = "eth_conf"
    config_name = "config.txt"
    coin = "eth"
    command = "SWITCHTOETH"
    execute = "start.bash"


@implementer(IPlugin, IMiner)
class AlgoClaymoreMiner(EthClaymoreMiner):

    pass


@implementer(IPlugin, IMiner)
class EtcClaymoreMiner(EthClaymoreMiner):
    coin = "etc"
    command = "SWITCHTOETC"


@implementer(IPlugin, IMiner)
class ExpClaymoreMiner(EthClaymoreMiner):
    coin = "exp"
    command = "SWITCHTOEXP"


@implementer(IPlugin, IMiner)
class MusicClaymoreMiner(EthClaymoreMiner):
    coin = "music"
    command = "SWITCHTOMUSIC"


@implementer(IPlugin, IMiner)
class UbqClaymoreMiner(EthClaymoreMiner):
    coin = "ubq"
    command = "SWITCHTOUBQ"


@implementer(IPlugin, IMiner)
class ZecClaymoreMiner:
    name = "claymore-zec"
    db = "zec_conf"
    config_name = "config.txt"
    coin = ""
    command = "SWITCHTOZEC"
    execute = "start.bash"
