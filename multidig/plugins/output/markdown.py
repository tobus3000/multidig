"""
Concrete Class for Output Plugin
Responsible for rendering of GUI output in "markdown" style.

Classes:
    Response
    ResponseBuilder
"""
import datetime
from pprint import pprint
from multidig.plugins.output import base_class

class MarkdownOutput(base_class.OutputPlugin):
    """Plugin class to render the query response in dig output format."""
    def __init__(self, **kwargs) -> None:
        """
        Init of Markdown Response Plugin

        :param **kwargs: Any key-word arguments supported by this class..
        :type **kwargs: dict
        """
        super().__init__(**kwargs)
        now = datetime.datetime.now()
        self.date_string = now.strftime("%c")
        self.parse_answers()

    def parse_answers(self):
        if self.dns_fqdn[-1] != ".":
            self.fqdn = f"{self.dns_fqdn}."

        # print(type(self.response))
        # pprint(vars(self.response))
        if self.response is None:
            return False
        return True

    def __str__(self):
        """Used to print the query response"""
        out_str = f"# Query Result for {self.fqdn}\n\n"
        out_str += f"Name Server: `{self.ns}`\n"
        out_str += f"Transport: {self.transport}\n"
        out_str += f"Query Time: `{self.query_time}` ms\n"
        out_str += f"Current Time: `{self.date_string}`\n"
        out_str += f"Response Code: `{self.response_rcode}`\n\n"
        out_str += "## QUESTION Section\n\nRequest for:\n"
        out_str += f"* Name: {self.fqdn}\n"
        out_str += f"* Record Type: {self.rr}\n"
        out_str += "\n## ANSWER Section\n\n"
        out_str += "## AUTHORITY Section\n\n"
        out_str += "## ADDITIONAL Section\n\n"
        # if not self.short:
            # out_str += self._section_header()
            # out_str += self._section_question()
            # out_str += self._section_answer()
            # out_str += self._section_footer()
        # else:
            # out_str = self._section_answer()
        return f"{out_str}\n---\n"

class MarkdownOutputBuilder(base_class.OutputPluginBuilder):
    """
    The Builder assures that we always only have
    one active plugin of the same type.
    """
    def __call__(self, fqdn, **kwargs):
        if not self._instance:
            self._instance = MarkdownOutput(**kwargs)
        return self._instance
