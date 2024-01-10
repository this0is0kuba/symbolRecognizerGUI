import customtkinter as ctk

from src.GUI.tabs.packTab import PackTab
from src.GUI.tabs.scriptTab import ScriptTab
from src.GUI.tabs.symbolTab import SymbolTab
from src.GUI.tabs.tabs import Tab


class MainPage:

    def __init__(self):

        # main appearance
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('dark-blue')

        # root parts:
        self.main_page = None
        self.sidebar = None
        self.main_content = None
        self.script_configurator_button = None
        self.symbol_configurator_button = None
        self.package_configurator_button = None
        self.top_content = None
        self.bottom_content = None

        # other parts
        self.script_tab: ScriptTab | None = None
        self.symbol_tab: SymbolTab | None = None
        self.pack_tab: PackTab | None = None

        # main parts
        self.root = ctk.CTk()
        self.root.title("Track Mouse App")
        self.root.geometry("1280x853")
        self.set_content()

        # functional parts
        self.current_tab_name = Tab.SCRIPT_TAB

    def set_content(self):

        self.main_page = ctk.CTkFrame(self.root)
        self.main_page.pack(fill='both', expand=True)

        self.set_sidebar()
        self.set_main_content()

    def set_sidebar(self):

        self.sidebar = ctk.CTkFrame(self.main_page, border_width=2)
        self.sidebar.pack(side=ctk.LEFT, fill="both")
        self.sidebar.propagate(False)
        self.sidebar.configure(width=300)

        self.set_sidebar_buttons()

    def set_main_content(self):

        self.main_content = ctk.CTkFrame(self.main_page)
        self.main_content.pack(side=ctk.LEFT, fill="both", expand=True)

        self.main_content.rowconfigure(0, weight=1)
        self.main_content.rowconfigure(1, weight=1)
        self.main_content.columnconfigure(0, weight=1)

        self.set_top_and_bottom_content()

    def set_sidebar_buttons(self):

        self.script_configurator_button = ctk.CTkButton(self.sidebar, text="Skrypty",
                                                        command=lambda: self.switch_tab(Tab.SCRIPT_TAB))
        self.script_configurator_button.pack(pady=(60, 10), fill='both', padx=10)

        self.symbol_configurator_button = ctk.CTkButton(self.sidebar, text="Gesty",
                                                        command=lambda: self.switch_tab(Tab.SYMBOL_TAB))
        self.symbol_configurator_button.pack(pady=10, fill='both', padx=10)

        self.package_configurator_button = ctk.CTkButton(self.sidebar, text="Pakiety",
                                                         command=lambda: self.switch_tab(Tab.PACK_TAB))
        self.package_configurator_button.pack(pady=10, fill='both', padx=10)

    def set_top_and_bottom_content(self):

        self.top_content = ctk.CTkFrame(self.main_content, border_width=2)
        self.top_content.grid(row=0, column=0, sticky="nsew")

        self.bottom_content = ctk.CTkFrame(self.main_content, border_width=2)
        self.bottom_content.grid(row=1, column=0, sticky="nsew")

        self.script_tab = ScriptTab(self.top_content, self.bottom_content, self.root)
        self.symbol_tab = SymbolTab(self.top_content, self.bottom_content, self.root)
        self.pack_tab = PackTab(self.top_content, self.bottom_content)

        self.script_tab.enable()

    def switch_tab(self, new_tab):

        if new_tab == self.current_tab_name:
            return

        match self.current_tab_name:

            case Tab.SCRIPT_TAB:
                self.script_tab.unable()

            case Tab.SYMBOL_TAB:
                self.symbol_tab.unable()

            case Tab.PACK_TAB:
                self.pack_tab.unable()

        match new_tab:

            case Tab.SCRIPT_TAB:
                self.script_tab.enable()
                self.current_tab_name = Tab.SCRIPT_TAB

            case Tab.SYMBOL_TAB:
                self.symbol_tab.enable()
                self.current_tab_name = Tab.SYMBOL_TAB

            case Tab.PACK_TAB:
                self.pack_tab.enable()
                self.current_tab_name = Tab.PACK_TAB

    def start_app(self):
        self.root.mainloop()
