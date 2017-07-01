from zope.interface import implementer
from twisted.plugin import IPlugin
from .base import IMiner


@implementer(IPlugin, IMiner)
class SGMiner:
    name = "sgminer-gm"
    db = "sgg_conf"
    config_name = "sg_miner.conf"
    coin = ""
    command = "SWITCHTOSGGM"
    execute = "sgminer-gm"
