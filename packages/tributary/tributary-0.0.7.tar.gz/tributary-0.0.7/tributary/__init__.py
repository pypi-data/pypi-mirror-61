from gevent import monkey
_PATCHED = False

if not _PATCHED:
    monkey.patch_all(thread=False, select=False)
    _PATCHED = True


from ._version import __version__  # noqa: F401
from .functional import pipeline, stop  # noqa: F401
