"""Module providing response section GUI element."""
import customtkinter
import pyperclip
from multidig.plugins import registry

DATA = "" # global var

class MyResponseFrame(customtkinter.CTkFrame):
    """Main Response Frame responsible for showing tabs for each plugin."""
    def __init__(self, master, title):
        super().__init__(master)
        # self.grid_columnconfigure(0, weight=1)
        self.title = customtkinter.CTkLabel(
            self,
            text=title,
            corner_radius=6
        )
        self.title.grid(
            row=0,
            column=0,
            padx=0,
            pady=(5,0),
            columnspan=2,
            sticky="ew"
        )
        # Add TabView
        self.tab_view = ResponseTabView(master=self)
        self.tab_view.grid(
            row=1,
            column=0,
            padx=5,
            pady=(0,0),
            sticky="ew"
        )

class ResponseTabView(customtkinter.CTkTabview):
    """Provides a tab for each output plugin."""
    def __init__(self, master, **kwargs):
        super().__init__(master)
        self.frames = {}
        # Add a tab for each plugin.
        for key in registry.output_plugins.list():
            self.add(key)
            self.tab(key).grid_columnconfigure(
                0,
                weight=1
            )
            self.frames[key] = TextOutputFrame(
                master=self.tab(key)
            )
            self.frames[key].grid(
                row=0,
                column=0,
                padx=10,
                pady=(0,5),
                sticky="ew"
            )
        # Set active tab to first plugin in the list.
        self.set(next(iter(self.frames)))

class TextOutputFrame(customtkinter.CTkFrame):
    """Provides the Dig Output Plugin tab"""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.cli_font = customtkinter.CTkFont(
            family="Courier New",
            size=11
        )
        self.textbox = customtkinter.CTkTextbox(
            master=self,
            height=450,
            width=650,
            corner_radius=0,
            font=self.cli_font
        )
        self.textbox.grid(
            row=1,
            column=0,
            padx=10,
            pady=(0, 10),
            columnspan=2,
            sticky="ew"
        )
        self.copy_all_button = customtkinter.CTkButton(
            self,
            text="Copy to Clipboard",
            command=self.copy_all
        )
        self.copy_all_button.grid(
            row=2,
            column=0,
            padx=(10,2),
            pady=(5,5),
            sticky="ew"
        )
        self.clear_textbox_button = customtkinter.CTkButton(
            self,
            text="Clear Output",
            command=self.clear_textbox
        )
        self.clear_textbox_button.grid(
            row=2,
            column=1,
            padx=(2,10),
            pady=(5,5),
            sticky="ew"
        )

    def clear_textbox(self):
        """Used to clear the textbox contents."""
        self.textbox.delete("0.0", "end")

    def copy_all(self):
        """Will copy the textbox content to the users clipboard."""
        global DATA # pylint: disable=global-statement
        self.textbox.focus()
        self.textbox.tag_add(
            "sel",
            "1.0",
            "end"
        )
        self.textbox.tag_config(
            "sel",
            background="#CAFFF9",
            foreground="black"
        )
        DATA = self.textbox.selection_get()
        pyperclip.copy(DATA)
