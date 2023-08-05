from __future__ import absolute_import

try:
    from ._version import version as __version__
except ImportError:
    __version__ = '0.0.0-dev0+Unknown'

from . import form, tstruct, solve, output
