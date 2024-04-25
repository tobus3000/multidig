"""
Concrete Class for Output Plugin
Responsible for rendering of GUI output in "dig" style.

Classes:
    DigOutput
    ResponseBuilder
"""
import datetime
import dns.edns
from pprint import pprint
from multidig.plugins.output import base_class
from multidig.helpers import utils
from multidig import __version__ # pylint: disable=no-name-in-module

class DigOutput(base_class.OutputPlugin):
    """Plugin class to render the query response in dig output format."""
    def __str__(self):
        """Used to print the query response"""
        pprint(vars(self))
        pprint(vars(self.response))
        out = []
        if not self.short:
            out.append(self._section_header())
        if not self.short:
            out.append(self._options())
        if not self.short:
            out.append(self._section_question())
        if len(self.response.answer) > 0:
            out.append(self._section_answer())
        if not self.short and len(self.response.authority) > 0:
            out.append(self._section_authority())
        if not self.short and len(self.response.additional) > 0:
            out.append(self._section_additional())
        if not self.short:
            out.append(self._section_footer())
        return "".join(out) + "\n" + "-" * 80 + "\n"

    def _options(self):
        show_opts = False
        if self.nsid:
            show_opts = True
        if self.ecs:
            show_opts = True
        if self.cookie:
            show_opts = True
        if show_opts is False:
            return ""
        out = [
            ";; OPT PSEUDOSECTION:",
            "; EDNS: version: 0, flags:; udp: 1232" #TODO: Use real numbers!
        ]
        for o in self.response.options:
            print(vars(o))
            if o.otype.value == dns.edns.NSID and self.nsid:
                out.append(f"; NSID: {o.data.hex(' ')} (\"{o.data.decode()}\")")
            if o.otype.value == dns.edns.COOKIE and self.cookie:
                if utils.compare_byte_string_prefix(self.cookie_value, o.data, 8):
                    cookie_check = "good"
                else:
                    cookie_check = "bad"
                out.append(f"; COOKIE: {o.data.hex()} ({cookie_check})") #TODO: replace "good" with validate value.
            if o.otype.value == dns.edns.ECS and self.ecs:
                out.append(f"; CLIENT-SUBNET: {o.address}/{o.srclen}/{o.scopelen}")
        return "\n".join(out) + "\n"

    def _section_header(self):
        out = [f"; <<>> MultiDig {__version__} <<>> {self.dns_fqdn} "]
        if not self.nsid and not self.ecs:
            out.append("+noedns +nocookie")
        else:
            out.append("+nocookie")
        if self.norec:
            out.append(" +norec")
        if self.nsid:
            out.append(" +nsid")
        if self.ecs:
            out.append(f" +subnet={self.ecs_subnet}")
        out.append("\n")
        out.append(";; global options: +cmd")
        out.append(";; Got answer:\n")
        out.append(f";; ->>HEADER<<- opcode: {self.response_opcode}, ")
        out.append(f"status: {self.response_rcode}, id: {self.response_id}\n")
        out.append(f";; flags: {self.response_flags.lower()}; ")
        out.append(f"QUERY: {len(self.response.question)}, ")
        out.append(f"ANSWER: {len(self.response.answer)}, ")
        out.append(f"AUTHORITY: {len(self.response.authority)}, ")
        out.append(f"ADDITIONAL: {len(self.response.additional)}\n")
        return "".join(out) + "\n"

    def _section_question(self):
        """Returns the QUESTION SECTION part."""
        out = [";; QUESTION SECTION:\n"]
        records = self.response.question
        for rec in records:
            out.append(f"{rec}\n")
        return "".join(out) + "\n"

    def _section_answer(self):
        out = []
        if not self.short:
            out.append(";; ANSWER SECTION:\n")
        records = self.response.answer
        for rec in records:
            if self.short:
                for r in rec:
                    out.append(f"{r}\n")
            else:
                out.append(f"{rec}\n")
        return "".join(out) + "\n"

    def _section_authority(self):
        out = [";; AUTHORITY SECTION:\n"]
        records = self.response.authority
        for rec in records:
            out.append(f"{rec}\n")
        return "".join(out) + "\n"

    def _section_additional(self):
        out = [";; ADDITIONAL SECTION:\n"]
        records = self.response.additional
        for rec in records:
            out.append(f"{rec}\n")
        return "".join(out) + "\n"

    def _section_footer(self):
        ns = self.ns
        now = datetime.datetime.now()
        date_string = now.strftime("%c")
        msg_size = len(self.response.to_wire())
        out = [
            f";; Query time: {round(self.query_time,4)} msec\n",
            f";; SERVER: {ns}#{self.ns_port}({ns})\n",
            f";; WHEN: {date_string}\n",
            f";; MSG SIZE  rcvd: {msg_size}"
        ]
        return "".join(out) + "\n"

class DigOutputBuilder(base_class.OutputPluginBuilder):
    """
    The Builder assures that we always get a new object
    for every Query Result.
    """
    def __call__(self, fqdn, **kwargs):
        self._instance = DigOutput(**kwargs)
        return self._instance
