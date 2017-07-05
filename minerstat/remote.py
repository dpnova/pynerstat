from zope.interface import implementer
from twisted.internet.interfaces import IProtocol
from minerstat.utils import Config
from typing import Tuple
from urllib import parse
import treq
from typing import Dict, Optional
import json
import asyncio
import platform
from twisted.logger import Logger
from twisted.plugin import getPlugins
from minerstat.miners.base import IMiner, MinerUtils
from minerstat.miners.claymore import AlgoClaymoreMiner


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
            body: Optional[str] = None
    ) -> str:
        """Make a request to the minerstat service."""
        url = self.make_full_url(resource)
        params = self.make_url_params(params=params)
        self.log.debug('Fetching: {0}'.format(url))
        self.log.debug('Fetching params: {0}'.format(str(params.items())))
        response = await self.treq.request(
            method=method,
            url=url,
            params=params,
            body=body)
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
        open(MinerUtils(coin, self.config).config_path(), 'w').write(content)

    async def send_log(self, res_data) -> None:
        await self.make_request(
            "POST", "getstat",
            body=json.dumps({"mes": res_data}))
        self.log.info("Package sent.")
        self.log.debug("Package sent: {data}", data=res_data)

    async def algo_check(self) -> None:
        futs = [
            self.get_request("bestquerytext"),
            self.get_request("bestquery"),
            self.get_request("dualresponse")
        ]
        bq, b, dr = await asyncio.gather(*futs)

    async def fetch_remote_command(self) -> Optional[Command]:
        content = await self.get_request(
            "control",
            params={"os": platform.system().lower()}
        )
        miner_coins = getPlugins(IMiner)  # Type: List[IMiner]
        for coin in miner_coins:
            if coin.command in content:
                return Command(coin.command, coin)
        if "REBOOT" in content:
            return Command("REBOOT", None)
        return None
