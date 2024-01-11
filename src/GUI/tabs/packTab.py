import customtkinter as ctk
import os
import math
import json

from src.classification.classifier import train_model


class PackTab:

    def __init__(self, top_content: ctk.CTkFrame, bottom_content: ctk.CTkFrame, root: ctk.CTk):

        self.root = root
        self.root_top_content = top_content
        self.root_bottom_content = bottom_content

        self.top_content: ctk.CTkFrame | None = None
        self.bottom_content: ctk.CTkFrame | None = None
        self.model_info: ctk.CTkTextbox | None = None
        self.selected_model = None

        self.directory = "../data/packs/models"
        self.directory_with_info = "../data/packs/modelsInfo"

        self.directory_with_symbol_info = "../data/symbols/symbolsInfo"
        self.directory_to_symbols = "../data/symbols/symbols"

        self.selected_pack = None
        self.packs = []
        self.find_all_packs()

        if len(self.packs) > 0:
            self.selected_pack = self.packs[0]

        self.set_top_content()
        self.set_bottom_content()

    def find_all_packs(self):

        if os.path.isdir(self.directory):
            self.packs = [pack.split('.')[0] for pack in os.listdir(self.directory)]
        else:
            self.packs = []

    def set_top_content(self):

        self.top_content = ctk.CTkFrame(self.root_top_content)

        for i in range(6):
            self.top_content.columnconfigure(i, weight=1)

        for i in range(math.ceil((len(self.packs) + 1) / 6)):
            self.top_content.rowconfigure(i, weight=1)

        self.top_content.grid_propagate(False)

        for i, pack in enumerate(self.packs):

            pack_button = ctk.CTkButton(self.top_content, text=pack,
                                        command=lambda current_pack=pack: self.switch_pack(current_pack))
            pack_button.grid(row=i//6, column=i % 6, sticky="nsew", padx=10, pady=10)

            if len(self.packs) < 6:
                pack_button.grid(pady=100)

        plus_pack_button = ctk.CTkButton(self.top_content, text="+", fg_color="green", hover_color='dark green',
                                         command=self.add_new_pack)
        plus_pack_button.grid(row=len(self.packs)//6, column=len(self.packs) % 6, sticky="nsew", padx=10, pady=10)

        if len(self.packs) < 6:
            plus_pack_button.grid(pady=100)

    def clear_top_content(self):
        self.top_content.destroy()

    def set_bottom_content(self):

        self.bottom_content = ctk.CTkFrame(self.root_bottom_content)

        self.bottom_content.columnconfigure(0, weight=8)
        self.bottom_content.columnconfigure(1, weight=1)
        self.bottom_content.rowconfigure(0, weight=1)

        self.bottom_content.propagate(False)

        self.set_config_buttons()

        self.model_info = ctk.CTkTextbox(self.bottom_content, font=("Helvetica", 18))
        self.set_model_info()
        self.model_info.grid(row=0, column=0, sticky='nsew')

    def set_config_buttons(self):

        button_frame = ctk.CTkFrame(self.bottom_content)
        button_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        button_frame.columnconfigure(0, weight=1)
        button_frame.rowconfigure(0, weight=5)
        button_frame.rowconfigure(1, weight=1)

        refresh_button = ctk.CTkButton(button_frame, text="Odśwież", command=self.refresh)
        refresh_button.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        delete_button = ctk.CTkButton(button_frame, text="Usuń Pakiet", fg_color="red", hover_color='dark red',
                                      command=lambda: delete_pack())
        delete_button.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        def delete_pack():

            os.remove(self.directory + "/" + self.selected_pack + ".h5")
            os.remove(self.directory_with_info + "/" + self.selected_pack + ".json")

            self.refresh()


    def find_script(self, symbol_name):

        with open(self.directory_with_symbol_info + "/" + symbol_name + ".json", 'r') as file:
            the_script = json.load(file)["script"]

        return the_script

    def set_model_info(self):

        all_symbols = self.find_model_info()["symbols"]
        all_scripts = []

        for symbol in all_symbols:
            all_scripts.append(self.find_script(symbol))

        info = "Dostępne symbole w wybranym modelu to: "

        for i in range(len(all_symbols)):

            info += "\n\n\t \u25CF " + all_symbols[i] + ":\t\t" + all_scripts[i]

        self.model_info.insert(ctk.END, info)
        self.model_info.configure(state=ctk.DISABLED)

    def find_model_info(self):

        with open(self.directory_with_info + "/" + self.selected_pack + ".json", 'r') as file:
            pack_info = json.load(file)

        return pack_info

    def switch_pack(self, clicked_pack):

        self.selected_pack = clicked_pack

        self.model_info.configure(state=ctk.NORMAL)
        self.model_info.delete('1.0', ctk.END)
        self.set_model_info()

    def add_new_pack(self):

        top_level_add_pack = ctk.CTkToplevel(self.root)
        top_level_add_pack.title("Nowy Pakiet")
        top_level_add_pack.geometry("400x500")

        self.root.eval(f'tk::PlaceWindow {str(top_level_add_pack)} center')

        label_script_name = ctk.CTkLabel(top_level_add_pack, text="Nazwa Pakietu:")
        label_script_name.pack(padx=10, pady=10)

        entry_script_name = ctk.CTkEntry(top_level_add_pack, placeholder_text="np. moj_pakiet")
        entry_script_name.pack(padx=10, pady=10)

        all_symbols = self.find_model_info()["symbols"]
        variables = []

        for symbol in all_symbols:

            var = ctk.StringVar()
            check_box = ctk.CTkCheckBox(top_level_add_pack, text=symbol, variable=var, onvalue=symbol, offvalue="")
            variables.append(var)

            check_box.pack(padx=10, pady=10)

        submit = ctk.CTkButton(top_level_add_pack, text="Zatwierdź",
                               command=lambda: self.create_new_pack(variables, entry_script_name.get(),
                                                                    top_level_add_pack))
        submit.pack(padx=10, pady=50)

        top_level_add_pack.attributes('-topmost', 'true')

    def create_new_pack(self, variables, new_pack_name,  window: ctk.CTkToplevel):

        if new_pack_name == "":
            return

        path_list = []
        selected_symbols = []

        for var in variables:
            if var.get() != "":

                selected_symbols.append(var.get())
                path_list.append(self.directory_to_symbols + "/" + var.get() + ".pkl")

        model, index_to_label = train_model(path_list)
        model.save(self.directory + "/" + new_pack_name + ".h5")

        model_info = {
            "symbols": selected_symbols,
            "index_to_label": index_to_label
        }

        with open(self.directory_with_info + "/" + new_pack_name + ".json", 'w') as f:
            json.dump(model_info, f)

        window.destroy()
        self.refresh()

    def refresh(self):

        self.find_all_packs()
        self.selected_pack = self.packs[0]

        self.clear_top_content()
        self.set_top_content()
        self.top_content.pack(fill='both', expand=True, padx=10, pady=10)

        self.model_info.configure(state=ctk.NORMAL)
        self.model_info.delete('1.0', ctk.END)

        self.set_model_info()

    def enable(self):

        self.top_content.pack(fill='both', expand=True, padx=10, pady=10)
        self.bottom_content.pack(fill='both', expand=True, padx=10, pady=10)

    def unable(self):

        self.top_content.pack_forget()
        self.bottom_content.pack_forget()