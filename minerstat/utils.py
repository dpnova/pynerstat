from typing import Generator
from twisted.internet import defer

InlineCallbacks = Generator[defer.Deferred, defer.Deferred, None]






