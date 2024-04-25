"""
Application Base Class for GUI.

Classes:
    App
    TabView
    DigFrame
"""
from ctypes import util
import customtkinter
from multidig import plugins, ui
from multidig.helpers import utils
from multidig.plugins import registry
from multidig import __version__ # pylint: disable=no-name-in-module

customtkinter.set_appearance_mode("system") # Modes: system, light, dark
customtkinter.set_default_color_theme("dark-blue") # Themes: blue, dark-blue, green

class App(customtkinter.CTk):
    """Main App and entry point of the GUI program."""
    def __init__(self):
        super().__init__()
        self.title(f"MultiDig - {__version__}")
        self.geometry("1000x660")
        self.grid_columnconfigure(0, weight=1)

        self.dig_frame = MainFrame(
            master=self,
            title="DNS Lookup"
        )
        self.dig_frame.grid(
            row=0,
            column=0,
            padx=0,
            pady=(5,0),
            sticky="ew"
        )

class MainFrame(customtkinter.CTkFrame):
    """Main app frame"""
    def __init__(self, master, title, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.query_frame = ui.search.MyQueryFrame(
            master=self,
            title=title
        )
        self.query_frame.grid(
            row=0,
            column=0,
            padx=5,
            pady=(5, 0),
            sticky="nsew"
        )
        self.transport_frame = ui.search.MyTransportFrame(
            master=self,
            title="Transport Type",
            values=[
                ("UDP", "udp"),
                ("TCP", "tcp"),
                ("TLS", "tls"),
                ("HTTPS", "https")
            ]
        )
        self.transport_frame.grid(
            row=1,
            column=0,
            padx=5,
            pady=(5,0),
            sticky="nsew"
        )
        self.response_frame = ui.response.MyResponseFrame(
            master=self,
            title="Response"
        )
        self.response_frame.grid(
            row=0,
            column=1,
            padx=5,
            pady=(5, 0),
            rowspan=2,
            sticky="nsew"
        )
        self.button = customtkinter.CTkButton(
            master=self,
            text="Query",
            command=self.query_button_callback
        )
        self.button.grid(
            row=3,
            column=0,
            columnspan=2,
            padx=5,
            pady=10,
            sticky="ew"
        )

    def query_button_callback(self):
        """The callback function called by clicking the Query button."""
        form = self.query_frame.get()
        plugin_args = form[1]
        # Validate the FQDN (or IP) input field.
        fqdn = form[0]
        if fqdn != "" and (utils.is_valid_hostname(fqdn) or utils.is_valid_ip(fqdn)):
            plugin_args['fqdn'] = fqdn
            self.query_frame.field_color("query", "#000000")
        else:
            self.query_frame.field_color("query", "#ff0000")
            return
        # Validate the name server fqdn or ip
        ns = form[1].get('ns','')
        if ns == "" or utils.is_valid_hostname(ns) or utils.is_valid_ip(ns):
            self.query_frame.field_color("nameserver", "#000000")
        else:
            self.query_frame.field_color("nameserver", "#ff0000")
            return
        func_str = self.transport_frame.get()
        if func_str == "":
            return
        plugin_args['transport'] = func_str
        self.query_record(**plugin_args)

    def query_record(self, **query_args):
        response_frame = {}
        q = plugins.registry.query_plugins.get('dns', **query_args)
        if q.query_dns():
            kwargs = q.to_dict()
            for key in registry.output_plugins.list():
                response_frame[key] = plugins.registry.output_plugins.get(key, **kwargs)
        else:
            for key in registry.output_plugins.list():
                if q.response is not None:
                    response_frame[key] = q.response
                else:
                    response_frame[key] = "An error has occured..."
        # Distribute response to output plugins.
        for key in registry.output_plugins.list():
            self.response_frame.tab_view.frames[key].textbox.insert(
                "0.end",
                text=f"{response_frame[key]}\n"
            )
