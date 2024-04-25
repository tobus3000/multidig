"""
UberDig - DNS Query Utility Package

Variables exported by this package:
    `__author__`: Provides the main package author.
    `__email__`: Author email address.
    `__version__`: Current version.
    `__all__`: A list of modules that can be used from this package.
"""
__author__ = "tobus3000"
__email__ = "tobus3000@tobotec.ch"
__version__ = "1.0.0"
__all__ = [
    "plugins",
    "ui",
    "__version__"
]

from .plugins import *
from .ui import *
