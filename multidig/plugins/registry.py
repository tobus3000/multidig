"""
Registered plugins to be used inside the application.

Classes:
    None
"""
from multidig.plugins import query, output
from multidig.helpers.factory import QueryPluginProvider, ResponsePluginProvider

query_plugins = QueryPluginProvider()
query_plugins.register_plugin('dns', query.dns.QueryBuilder())

output_plugins = ResponsePluginProvider()
output_plugins.register_plugin('dig', output.dig.DigOutputBuilder())
output_plugins.register_plugin('markdown', output.markdown.MarkdownOutputBuilder())
