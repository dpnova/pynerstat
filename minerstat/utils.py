from typing import Generator
from twisted.internet import defer
from configparser import ConfigParser
import os.path
from typing import Optional

InlineCallbacks = Generator[defer.Deferred, defer.Deferred, None]


class ConfigParseError(Exception):

    pass


class Config:

    def __init__(
            self,
            client: str,
            accesskey: str,
            worker: str,
            path: str,
            db: Optional[str] = None,
            api_base: str = "https://minerstat.com/",
    ) -> None:
        self.client = client
        self.db = db
        if not db:
            if client == "claymore-eth":
                self.db = "eth_conf"
            elif client == "claymore-zec":
                self.db = "zec_conf"
            elif client == "ewbf-zec":
                self.db = "ezec_conf"
            elif client == "sgminer-gm":
                self.db = "sgg_conf"
        self.accesskey = accesskey
        self.worker = worker
        self.path = path
        self.api_base = api_base

    @classmethod
    def from_configparser(cls, parser: ConfigParser, section: str):
        conf = parser[section]
        if "path" not in conf:
            conf['path'] = os.path.join(os.path.dirname(__file__), "..")
        self = cls(**dict(conf))
        return self

    @classmethod
    def from_path(cls, path: str, section: str):
        parser = ConfigParser()
        parser.read(path)
        try:
            return cls.from_configparser(parser, section)
        except TypeError as e:
            raise ConfigParseError("Invalid config [{}]".format(e))

    @classmethod
    def default(cls):
        return cls(
            client="algo",
            accesskey="1234",
            worker="rig2",
            path=os.path.dirname(os.path.join(__file__, "..", "..")))
