from zope.interface import implementer

from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker

from minerstat.service import MinerStatService
from minerstat.rig import Rig


class Options(usage.Options):
    optParameters = [["port", "p", 1235, "The port number to listen on."]]


@implementer(IServiceMaker, IPlugin)
class MinerServiceMaker(object):
    tapname = "minerstat-linux"
    description = "minerstat-linux implmentation in python"
    options = Options

    def makeService(self, options: usage.Options):
        """
        Construct a minerstat server.
        """
        rig = Rig()
        return MinerStatService(rig)


# Now construct an object which *provides* the relevant interfaces
# The name of this variable is irrelevant, as long as there is *some*
# name bound to a provider of IPlugin and IServiceMaker.

serviceMaker = MinerServiceMaker()
