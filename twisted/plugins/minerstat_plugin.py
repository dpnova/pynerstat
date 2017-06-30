from zope.interface import implementer

from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker

from minerstat.service import MinerStatService
from minerstat.rig import Rig
from minerstat.utils import Config


class Options(usage.Options):
    optParameters = [
        ["config", "c", "config.ini", "Load config from here."],
        ["section", "s", "main", "Use this section of the config."]
    ]


@implementer(IServiceMaker, IPlugin)
class MinerServiceMaker(object):
    tapname = "minerstat-linux"
    description = "minerstat-linux implmentation in python"
    options = Options

    def makeService(self, options: usage.Options):
        """
        Construct a minerstat server.
        """
        config_path = options.get("config")  # Type: str
        config_section = options.get("section")  # Type: str
        config = Config.from_path(config_path, config_section)
        rig = Rig(config)
        return MinerStatService(rig)


# Now construct an object which *provides* the relevant interfaces
# The name of this variable is irrelevant, as long as there is *some*
# name bound to a provider of IPlugin and IServiceMaker.

serviceMaker = MinerServiceMaker()
