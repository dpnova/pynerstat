from zope.interface import implementer
from twisted.internet.interfaces import IProtocol
from minerstat.utils import Config
from typing import Tuple, Union
from urllib import parse
import treq
from typing import Dict, Optional
import platform
from twisted.logger import Logger
from twisted.plugin import getPlugins
from minerstat.miners.base import IMiner, MinerUtils
from minerstat.miners.claymore import AlgoClaymoreMiner
from twisted.internet import defer


class Command:
    def __init__(self, command_name: str, coin: Optional[IMiner]) -> None:
        self.command_name = command_name
        self.coin = coin


@implementer(IProtocol)
class MinerStatRemoteProtocol:
    log = Logger()

    def __init__(self, config: Config, treq=treq) -> None:
        self.config = config
        self.treq = treq

    def make_full_url(self, component: str) -> str:
        return parse.urljoin(
            self.config.api_base, component + ".php"
        )

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
            headers: Optional[Dict[str, str]] = None,
            data: Optional[Union[str, Dict[str, str]]] = None
    ) -> str:
        """Make a request to the minerstat service."""
        url = self.make_full_url(resource)
        params = self.make_url_params(params=params)
        self.log.debug(
            'Fetching: {0}:  {1} with params: {2}'.format(
                method, url, str(params.items())))
        response = await self.treq.request(
            method=method,
            url=url,
            params=params,
            data=data,
            headers=headers,
            browser_like_redirects=True)
        content = await response.text()
        return content

    async def get_request(
            self,
            resource,
            params: Optional[Dict[str, str]] = None,
    ) -> str:
        """Make a get request to the minerstat service."""
        content = await self.make_request("GET", resource, params)
        return content

    async def algoinfo(self) -> Tuple[str, str]:
        algoinfo = await self.get_request("bestquery")
        dualresponse = await self.get_request("dualresponse")
        return (algoinfo, dualresponse)

    async def dlconf(self, coin: IMiner) -> None:
        content = await self.get_request("getresponse", params={
            "db": coin.db,
            "action": "config",
            "coin": coin.coin,
            "algo": "yes" if isinstance(coin, AlgoClaymoreMiner) else "no"})
        self.log.debug("writing config path: {0}".format(
            MinerUtils(coin, self.config).config_path()))
        open(MinerUtils(coin, self.config).config_path(), 'w').write(
            coin.config_template.format(content))

    async def send_log(self, res_data) -> None:
        if not res_data:
            self.log.warn("Logs for server are empty now.")
            return
        await self.make_request(
            "POST", "getstat",
            data={"mes": res_data})
        self.log.info("Package sent.")
        self.log.debug("Package sent: {data}", data=repr(res_data))

    async def algo_check(self) -> Tuple[str, str, str]:
        futs = [
            self.get_request("bestquerytext"),
            self.get_request("bestquery"),
            self.get_request("dualresponse")
        ]
        bqt, bq, dr = await defer.DeferredList([
            defer.ensureDeferred(f) for f in futs])
        return (bqt, bq, dr)

    async def fetch_remote_command(self, coin: IMiner) -> Optional[Command]:
        content = await self.get_request(
            "control",
            params={
                "worker": "{}.{}".format(
                    self.config.accesskey,
                    self.config.worker),
                "miner": coin.name,
                "os": platform.system().lower()},
        )
        self.log.debug("remote command: {}".format(repr(content)))
        miner_coins = getPlugins(IMiner)  # Type: List[IMiner]
        for coin in miner_coins:
            if coin.command in content:
                return Command(coin.command, coin)
        if "REBOOT" in content:
            return Command("REBOOT", None)
        return None

    async def announce(self, coin: IMiner) -> str:
        content = await self.make_request(
            "POST",
            "control",
            params={
                "worker": "{}.{}".format(
                    self.config.accesskey,
                    self.config.worker),
                "miner": coin.name,
                "os": platform.system().lower()},
            data={"mes": ""}
        )
        return content
