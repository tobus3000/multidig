"""
Abstract Base Class for Output Plugins.

Classes:
    OutputPlugin
    OutputPluginBuilder
"""
from abc import ABCMeta
import dns.opcode
import dns.rcode
import dns.flags
import dns.message

class OutputPlugin(metaclass=ABCMeta):
    """Generic Output Plugin Abstract Base Class"""

    def __init__(self, **kwargs) -> None:
        """
        Init function of the Query ABC base class.
        We expect a `dns.message.QueryMessage` in the response property.
        """
        self.fqdn = kwargs.get('fqdn', None)
        self.dns_fqdn = kwargs.get('dns_fqdn', None)
        self.rr = kwargs.get('rr', None)
        self.short = kwargs.get('short', False) # Short option value. Default to False.
        self.norec = kwargs.get('norec', False) # Set the recursion desired flag. Defaults to False.
        self.nsid = kwargs.get('nsid', False) # EDNS NSID flag.
        self.ecs = kwargs.get('ecs', False) # EDNS Client Subnet option.
        self.ecs_subnet = kwargs.get('ecs_subnet', None)
        self.cookie = kwargs.get('cookie', False)
        self.cookie_value = kwargs.get('cookie_value', None)
        self.transport = kwargs.get('transport', "n/a")
        self.ns = kwargs.get('ns', None)
        self.ns_port = kwargs.get('ns_port', None)
        self.response = kwargs.get('response', None)
        self.query_time = kwargs.get('query_time', 0)
        # Extract key elements of response data for better accessibility.
        self.response_flags = ""
        self.response_opcode = ""
        self.response_rcode = ""
        if isinstance(self.response, dns.message.QueryMessage):
            self.response_id = self.response.id
            self._parse_flags(self.response.flags)
        else:
            raise NotImplementedError("Can only process `dns.message.QueryMessage` objects.")

    def _parse_flags(self, flags):
        """Parse the message flags and assign to instance variables."""
        self.response_flags = dns.flags.to_text(flags)
        self.response_opcode = dns.opcode.to_text(dns.opcode.from_flags(flags))
        self.response_rcode = dns.rcode.to_text(dns.rcode.from_flags(flags,0))

class OutputPluginBuilder(metaclass=ABCMeta):
    """Builder for the OutputPlugin abstract base class."""
    def __init__(self):
        self._instance = None
