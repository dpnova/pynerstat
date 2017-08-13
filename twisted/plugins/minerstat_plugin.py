from zope.interface import implementer

from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker

from minerstat.service import MinerStatService
from minerstat.rig import Rig
from minerstat.utils import Config
from minerstat.remote import MinerStatRemoteProtocol

from minerstat.miners.claymore import EthClaymoreMiner
from minerstat.miners.claymore import EtcClaymoreMiner
from minerstat.miners.claymore import ExpClaymoreMiner
from minerstat.miners.claymore import MusicClaymoreMiner
from minerstat.miners.claymore import UbqClaymoreMiner
from minerstat.miners.claymore import ZecClaymoreMiner
from minerstat.miners.claymore import AlgoClaymoreMiner
from minerstat.miners.claymore import DualClaymoreMiner


from minerstat.miners.ewbf import EWBFZecMiner
from minerstat.miners.sgminer import SGMiner
import os.path

eth = EthClaymoreMiner()
etc = EtcClaymoreMiner()
exp = ExpClaymoreMiner()
music = MusicClaymoreMiner()
ubq = UbqClaymoreMiner()
zec = ZecClaymoreMiner()
ewbf = EWBFZecMiner()
sg = SGMiner()
algo = AlgoClaymoreMiner()
dual = DualClaymoreMiner()


class Options(usage.Options):
    optParameters = [
        ["config", "c", "~/.minerstat/config.ini", "Load config from here."],
        ["section", "s", "main", "Use this section of the config."]
    ]


@implementer(IServiceMaker, IPlugin)
class MinerServiceMaker:
    tapname = "minerstat-linux"
    description = "minerstat-linux implmentation in python"
    options = Options

    def makeService(self, options: usage.Options):
        """
        Construct a minerstat server.
        """
        config_path = options.get("config")  # Type: str
        config_path = os.path.expanduser(config_path)
        config_section = options.get("section")  # Type: str
        config = Config.from_path(config_path, config_section)
        remote = MinerStatRemoteProtocol(config)
        rig = Rig(config, remote)
        return MinerStatService(rig)


# Now construct an object which *provides* the relevant interfaces
# The name of this variable is irrelevant, as long as there is *some*
# name bound to a provider of IPlugin and IServiceMaker.

serviceMaker = MinerServiceMaker()
