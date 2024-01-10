import customtkinter as ctk
import os
import math


class PackTab:

    def __init__(self, top_content: ctk.CTkFrame, bottom_content: ctk.CTkFrame):

        self.top_content = ctk.CTkFrame(top_content)
        self.bottom_content = ctk.CTkFrame(bottom_content)

        self.directory = "../data/packs/models"
        self.directory_with_info = "../data/packs/modelsInfo"
        self.packs = self.find_all_packs()

        self.set_top_content()
        self.set_bottom_content()

    def find_all_packs(self):
        if os.path.isdir(self.directory):
            return os.listdir(self.directory)

        return []

    def set_top_content(self):

        for i in range(6):
            self.top_content.columnconfigure(i, weight=1)

        for i in range(math.ceil((len(self.packs) + 1) / 6)):
            self.top_content.rowconfigure(i, weight=1)

        self.top_content.grid_propagate(False)

        for i, pack in enumerate(self.packs):

            pack_button = ctk.CTkButton(self.top_content, text=pack)
            pack_button.grid(row=i//6, column=i % 6, sticky="nsew", padx=10, pady=10)

            if len(self.packs) < 6:
                pack_button.grid(pady=100)

        plus_pack_button = ctk.CTkButton(self.top_content, text="+", fg_color="green")
        plus_pack_button.grid(row=len(self.packs)//6, column=len(self.packs) % 6, sticky="nsew", padx=10, pady=10)

        if len(self.packs) < 6:
            plus_pack_button.grid(pady=100)


    def set_bottom_content(self):
        pass

    def enable(self):

        self.top_content.pack(fill='both', expand=True, padx=10, pady=10)
        self.bottom_content.pack(fill='both', expand=True, padx=10, pady=10)

    def unable(self):

        self.top_content.pack_forget()
        self.bottom_content.pack_forget()
