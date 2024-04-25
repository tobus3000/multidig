"""
UberDig - Plugin Summary Sub-Package

Variables exported by this package:
    `__all__`: A list of modules that can be used from this package.
"""
__all__ = [
    "query",
    "output",
    "query_plugins",
    "output_plugins"
]

from multidig.plugins import query
from multidig.plugins import output
from multidig.plugins.registry import query_plugins, output_plugins
