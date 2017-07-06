from zope.interface import Interface, Attribute
from minerstat.utils import Config
import os.path


class IMiner(Interface):

    name = Attribute("The name of the miner.")  # Type: str
    db = Attribute("The DB server side?")  # Type: str
    config_name = Attribute("The config file name for miner.")  # Type: str
    coin = Attribute("Which coin param to send the miner.")  # Type: str
    command = Attribute("Command used to switch to this.")  # Type: str
    execute = Attribute("The executable for the miner.")  # Type: str

    def fetch_logs():  # noqa
        """Fetch logs from the process."""


class MinerUtils:

    def __init__(self, coin: IMiner, config: Config) -> None:
        self.coin = coin
        self.config = config

    def miner_path(self) -> str:
        return os.path.join(
            self.config.path,
            "clients",
            self.coin.folder_name)

    def config_path(self) -> str:
        return os.path.join(
            self.miner_path(),
            self.coin.config_name)

    def executable_path(self) -> str:
        return os.path.join(
            self.miner_path, self.coin.execute)
