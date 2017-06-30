from twisted.trial import unittest
from minerstat.utils import Config, ConfigParseError


class ConfigTest(unittest.TestCase):

    def test_default(self):
        default = Config.default()
        self.assertEqual(default.worker, "rig2")

    def test_from_path_bad_conf(self):
        open("config.ini", 'w').write("""
        [main]
        foo=bar
        """)
        self.assertRaises(
            ConfigParseError, Config.from_path, "config.ini", "main")

    def test_from_path_not_enough(self):
        open("config.ini", 'w').write("""
        [main]
        client=1234
        """)
        self.assertRaises(
            ConfigParseError, Config.from_path, "config.ini", "main")

    def test_from_path(self):
        open("config.ini", 'w').write("""
        [main]
        client=1234
        accesskey=foo
        worker=rig2
        db=eth_conf
        coin=eth
        file=foo.txt
        path=foobar
        """)
        config = Config.from_path("config.ini", "main")
        self.assertTrue(config)
