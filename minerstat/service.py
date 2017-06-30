from twisted.application.service import Service
from twisted.internet import defer
from zope.interface import implementer
from twisted.internet.interfaces import IProtocol
from minerstat.rig import Rig
from minerstat.utils import Config
from urllib import parse
import treq
from typing import Dict, Optional


@implementer(IProtocol)
class MinerStatRemoteProtocol:
    def __init__(self, config: Config, treq=treq) -> None:
        self.config = config
        self.treq = treq

    def make_full_url(self, component: str) -> str:
        return parse.urljoin(
            self.config.api_url, component + ".php?"
        ) + parse.urlencode(self.make_url_params())

    def make_url_params(
            self,
            params: Optional[Dict[str, str]] = None
    ) -> Dict[str, str]:
        new_params = {
            "token": self.config.accesskey,
            "worker": self.config.worker
        }
        if params:
            new_params.update(params)
        return new_params

    async def make_request(
            self,
            method: str,
            resource: str,
            params: Optional[Dict[str, str]] = None,
            body: Optional[str] = None
    ) -> str:
        url = self.make_full_url(resource)
        params = self.make_url_params()
        response = await self.treq.request(
            method=method,
            url=url,
            params=params,
            body=body)
        content = await response.content()
        return content

    async def get_request(
            self,
            resource,
            params: Optional[Dict[str, str]] = None,
    ) -> str:
        content = await self.make_request("GET", resource, params)
        return content

    async def algoinfo(self) -> str:
        content = await self.get_request("bestquery")
        return content

    def dlconf(self):
        pass

    def send_log(self):
        pass

    def algo_check(self):
        pass

    def dispatch_remote_command(self):
        pass

    def poll_remote(self):
        pass


class MinerStatService(Service):
    def __init__(self, rig: Rig) -> None:
        self.rig = rig

    def startService(self) -> None:
        self.rig.start()

    def stopService(self) -> None:
        return defer.ensureDeferred(self.rig.stop())
