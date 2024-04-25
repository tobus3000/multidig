"""
Concrete Class for DNS Queries.
Holds a Query sub-class used to resolve standard DNS queries based on RFC1035.
https://www.rfc-editor.org/rfc/rfc1035

Classes:
    Query
"""
from datetime import datetime
import dns.resolver
import dns.reversename
import dns.message
import dns.rdataclass
import dns.flags
import dns.query
import dns.edns
from multidig.plugins.query import base_class
from multidig.helpers import utils

class Query(base_class.QueryPlugin):
    """Plugin class to use standard DNS protocol to query for a DNS name."""
    def __init__(self, **kwargs) -> None:
        """
        Init of DNS Plugin class.

        :param fqdn: The fully-qualified domain name to be queried for.
        :type fqdn: str
        :param **kwargs: Any key-word arguments supported by this class..
        :type **kwargs: dict
        """
        super().__init__(**kwargs)
        self.setup()

    def setup(self) -> None:
        """Post init setup to configure plugin specific defaults and settings."""
        self.resolver = dns.resolver.Resolver()
        self.ns_port = self.resolver.port
        if self.ns is not None:
            self.resolver.nameservers = [self.ns]

    def query_dns(self):
        success = True
        # define name server to query
        if self.ns is None:
            self.ns = self.resolver.nameservers[0]
        query = dns.message.make_query(self.dns_fqdn, self.rr, dns.rdataclass.IN)

        # EDNS and other options
        use_opts = False
        opts = []
        if self.nsid:
            use_opts = True
            opts.append(dns.edns.GenericOption(dns.edns.OptionType.NSID, b""))

        if self.ecs and self.ecs_subnet:
            use_opts = True
            opts.append(dns.edns.ECSOption.from_text(self.ecs_subnet))

        #TODO: Cookie option
        if self.cookie:
            use_opts = True
            self.cookie_value = utils.generate_client_cookie()
            opts.append(
                dns.edns.GenericOption(
                    dns.edns.OptionType.COOKIE, self.cookie_value
                )
            )

        if use_opts:
            query.use_edns(0, options=opts)

        # disable recursion if 'no recursion' is selected.
        if self.norec:
            query.flags ^= dns.flags.RD

        # prepare transport
        transport = getattr(dns.query, self.transport)

        # run the query
        start_time = datetime.now()
        try:
            self.response = transport(query, self.ns)
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
            pass
        except Exception as error:
            self.response = f"error: {error}"
            success = False
        self.query_time = datetime.now() - start_time
        return success

class QueryBuilder(base_class.QueryPluginBuilder):
    """
    The Builder assures that we always get a new object
    for each Query.
    """
    def __call__(self, **kwargs):
        self._instance = Query(**kwargs)
        return self._instance
