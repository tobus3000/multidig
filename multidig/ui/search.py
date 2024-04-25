import customtkinter

class MyQueryFrame(customtkinter.CTkFrame):
    """Defines the Query portion of the GUI."""
    def __init__(self, master, title):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.title= customtkinter.CTkLabel(self, text=title, corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="ew")
        # FQDN Field
        self.label_fqdn = customtkinter.CTkLabel(self, text="FQDN or IP", fg_color="transparent")
        self.label_fqdn.grid(row=1, column=0, padx=10, pady=(0, 0), sticky="w")
        self.entry_fqdn = customtkinter.CTkEntry(self, placeholder_text="server.domain.net", width=240)
        self.entry_fqdn.grid(row=2, column=0, padx=10, pady=(0, 0), sticky="w")
        # Nameserver Field
        self.label_ns = customtkinter.CTkLabel(self, text="Nameserver", fg_color="transparent")
        self.label_ns.grid(row=3, column=0, padx=10, pady=(0, 0), sticky="w")
        self.entry_ns = customtkinter.CTkEntry(self, placeholder_text="leave blank for default resolver", width=240)
        self.entry_ns.grid(row=4, column=0, padx=10, pady=(0, 0), sticky="w")
        # Record Type
        self.rr_option = customtkinter.CTkOptionMenu(self, values=['A', 'CNAME', 'TXT', 'PTR', 'MX', 'NS', 'SOA'], width=240)
        self.rr_option.set("A")
        self.rr_option.grid(row=5, column=0, padx=10, pady=(10,0), sticky="w")
        # Options
        self.checkbox_short = customtkinter.CTkCheckBox(self, text="Short answer (+short)", hover=True)
        self.checkbox_short.deselect()
        self.checkbox_short.grid(row=6, column=0, padx=10, pady=(5,0), sticky="w")
        self.checkbox_norec = customtkinter.CTkCheckBox(self, text="No recursion (+norec)", hover=True)
        self.checkbox_norec.deselect()
        self.checkbox_norec.grid(row=7, column=0, padx=10, pady=(5,0), sticky="w")
        self.checkbox_nsid = customtkinter.CTkCheckBox(self, text="NSID Option (+nsid)", hover=True)
        self.checkbox_nsid.deselect()
        self.checkbox_nsid.grid(row=8, column=0, padx=10, pady=(5,0), sticky="w")
        self.ecs_subnet = ""
        self.checkbox_ecs = customtkinter.CTkCheckBox(self, text="ECS Option (+subnet)", hover=True, command=self.config_ecs)
        self.checkbox_ecs.deselect()
        self.checkbox_ecs.grid(row=9, column=0, padx=10, pady=(5,0), sticky="w")
        self.checkbox_cookie = customtkinter.CTkCheckBox(self, text="DNS Cookie (+cookie)", hover=True)
        self.checkbox_cookie.deselect()
        self.checkbox_cookie.grid(row=10, column=0, padx=10, pady=(5,0), sticky="w")

    def config_ecs(self):
        """Open dialog to configure ECS subnet."""
        dialog = customtkinter.CTkInputDialog(
            title = "EDNS Client Subnet",
            text = "Provide client subnet: a.b.c.d/24 or a.b.c.d/24/32"
        )
        self.ecs_subnet = dialog.get_input()


    def get(self):
        return (
            self.entry_fqdn.get(),
            {
                'rr': self.rr_option.get(),
                'short': self.checkbox_short.get(),
                'norec': self.checkbox_norec.get(),
                'ns': self.entry_ns.get(),
                'nsid': self.checkbox_nsid.get(),
                'ecs': self.checkbox_ecs.get(),
                'ecs_subnet': self.ecs_subnet,
                'cookie': self.checkbox_cookie.get()
            }
        )
    
    def field_color(self, field: str, color: str):
        if field == "query":
            self.entry_fqdn.configure(
                text_color=color
            )
        elif field == "nameserver":
            self.entry_ns.configure(
                text_color=color
            )

class MyTransportFrame(customtkinter.CTkFrame):
    """Defines the Transport section of the GUI."""
    def __init__(self, master, title, values):
        super().__init__(master)
        self.rb_list = []
        self.rb_func = customtkinter.StringVar(value="")
        self.grid_columnconfigure(0, weight=1)
        self.title= customtkinter.CTkLabel(self, text=title, corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="ew")
        # Radio Buttons
        for i, value in enumerate(values):
            text, func = value
            rb = customtkinter.CTkRadioButton(
                self,
                text=text,
                hover=True,
                variable=self.rb_func,
                value=func
            )
            rb.grid(
                row=i+1,
                column=0,
                padx=10,
                pady=(0,5),
                sticky="w"
            )
            self.rb_list.append(rb)
        self.rb_list[0].select()

    def get(self):
        return self.rb_func.get()
    
    def set(self, value):
        self.rb_func.set(value)