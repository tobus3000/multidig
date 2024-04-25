"""
Abstract Base Class for DNS Queries.

Classes:
    QueryPlugin
    QueryPluginBuilder
"""
from abc import ABCMeta, abstractmethod
import dns.reversename
import dns.query

class QueryPlugin(metaclass=ABCMeta):
    """Generic Query Class"""

    def __init__(self, **kwargs) -> None:
        """
        Init function of the Query ABC base class.

        :param fqdn: The fully-qualified domain name to be queried for.
        :type fqdn: str
        :param **kwargs: Any key-word arguments supported by this class..
        :type **kwargs: dict
        """
        super().__init__()
        self.fqdn = kwargs.get('fqdn', None)
        self.dns_fqdn = self.fqdn
        self.rr = kwargs.get('rr', "A") # Defalt to A RR if no other option is chosen.
        if self.rr == "PTR":
            self.dns_fqdn = dns.reversename.from_address(self.fqdn)
        self.resolver = "" # The DNS resolver to be used.
        self.resolve_func = None # An alias to the resolver function (eg. dns.query.udp)
        self.short = kwargs.get('short', False) # Short option value. Default to 1 if none.
        self.norec = kwargs.get('norec', False) # Set the recursion desired flag. Defaults to False.
        self.nsid = kwargs.get('nsid', False) # Set EDNS NSID option.
        self.ecs = kwargs.get('ecs', False)
        self.ecs_subnet = kwargs.get('ecs_subnet', None)
        self.cookie = kwargs.get('cookie', False)
        self.cookie_value = None
        self.transport = kwargs.get('transport', "udp") # Set UDP unless other transport is selected.
        self.ns = kwargs.get('ns', None)
        self.ns_port = kwargs.get('ns_port', None)
        self.query_time = float()
        if self.ns == "":
            self.ns = None
        self.response = None # list of dicts: {name, target, type, ttl}

    @abstractmethod
    def setup(self):
        """Plugin specific setup routine to configure default resolver, etc."""

    @abstractmethod
    def query_dns(self) -> bool:
        """
        Run the DNS query against the chosen name server.

        :return: True or False based on the outcome of the query.
        :rypte: bool
        """
        query_status = True
        return query_status

    def to_dict(self):
        """Return key elements of the object in a dictionary."""
        out_dict = {
            "fqdn": self.fqdn,
            "dns_fqdn": self.dns_fqdn,
            "rr": self.rr,
            "response": self.response,
            "short": self.short,
            "norec": self.norec,
            "transport": self.transport,
            "ns": self.ns,
            "ns_port": self.ns_port,
            "nsid": self.nsid,
            "ecs": self.ecs,
            "ecs_subnet": self.ecs_subnet,
            "cookie": self.cookie,
            "cookie_value": self.cookie_value
        }
        return out_dict


class QueryPluginBuilder(metaclass=ABCMeta):
    """Builder for the QueryPlugin abstract base class."""
    def __init__(self):
        self._instance = None
