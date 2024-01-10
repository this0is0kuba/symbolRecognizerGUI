import customtkinter as ctk
import os
import math
from PIL import Image
import json
import pickle

from src.dataCollectionTool.paint.paintGUI import PaintGUI


class SymbolTab:

    def __init__(self, top_content: ctk.CTkFrame, bottom_content: ctk.CTkFrame, root):

        self.root = root
        self.root_top_content = top_content
        self.root_bottom_content = bottom_content

        self.top_content = None
        self.bottom_content = None
        self.img_label: ctk.CTkLabel | None = None

        self.directory = "../data/symbols/symbols"
        self.directory_with_info = "../data/symbols/symbolsInfo"
        self.directory_with_images = "../data/symbols/symbolImages"

        self.selected_symbol = None
        self.symbols = []
        self.find_all_symbols()

        if len(self.symbols) > 0:
            self.selected_symbol = self.symbols[0]

        self.set_top_content()
        self.set_bottom_content()

    def find_all_symbols(self):

        if os.path.isdir(self.directory):
            self.symbols = [symbol.split(".")[0] for symbol in os.listdir(self.directory)]
        else:
            self.symbols = []

    def set_top_content(self):

        self.top_content = ctk.CTkFrame(self.root_top_content)

        for i in range(6):
            self.top_content.columnconfigure(i, weight=1)

        for i in range(math.ceil((len(self.symbols) + 1) / 6)):
            self.top_content.rowconfigure(i, weight=1)

        self.top_content.grid_propagate(False)

        for i, symbol in enumerate(self.symbols):

            symbol_name = symbol.split(".")[0]

            try:
                img = Image.open(self.directory_with_images + "/" + symbol_name + ".png")
                symbol_image = ctk.CTkImage(img, size=(80, 80))

            except FileNotFoundError:
                symbol_image = None

            symbol_button = ctk.CTkButton(self.top_content, image=symbol_image, compound="top", text=symbol_name,
                                          command=lambda current_symbol=symbol: self.switch_symbol(current_symbol))
            symbol_button.grid(row=i // 6, column=i % 6, sticky="nsew", padx=10, pady=10)

            if len(self.symbols) < 6:
                symbol_button.grid(pady=100)

        plus_symbol_button = ctk.CTkButton(self.top_content, text="+", fg_color="green",
                                                command=self.add_new_symbol)
        plus_symbol_button.grid(row=len(self.symbols) // 6, column=len(self.symbols) % 6, sticky="nsew", padx=10,
                                     pady=10)

        if len(self.symbols) < 6:
            plus_symbol_button.grid(pady=100)

    def clear_top_content(self):
        self.top_content.destroy()

    def set_bottom_content(self):

        self.bottom_content = ctk.CTkFrame(self.root_bottom_content)

        self.bottom_content.columnconfigure(0, weight=3)
        self.bottom_content.columnconfigure(1, weight=1)
        self.bottom_content.rowconfigure(0, weight=1)

        self.bottom_content.grid_propagate(False)

        symbol_name = self.selected_symbol

        # if self.img_label is not None:
        #     self.img_label.destroy()

        try:
            img = Image.open(self.directory_with_images + "/" + symbol_name + ".png")
            symbol_image = ctk.CTkImage(img, size=(500, 500))
            self.img_label = ctk.CTkLabel(self.bottom_content, image=symbol_image, text="")

        except FileNotFoundError:
            self.img_label.destroy()
            self.img_label = ctk.CTkLabel(self.bottom_content, image=None, text="")

        self.img_label.grid(row=0, column=0)

        self.set_config_buttons()

    def clear_bottom_content(self):
        self.bottom_content.destroy()

    def set_config_buttons(self):

        def change_script(choice):

            with open(self.directory_with_info + "/" + self.selected_symbol + ".json", 'r') as file:

                symbol_info = json.load(file)
                symbol_info["script"] = choice

                with open(self.directory_with_info + "/" + self.selected_symbol + ".json", 'w') as f:
                    json.dump(symbol_info, f)

        button_frame = ctk.CTkFrame(self.bottom_content)
        button_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        button_frame.columnconfigure(0, weight=1)
        button_frame.rowconfigure(0, weight=1)
        button_frame.rowconfigure(1, weight=2)
        button_frame.rowconfigure(2, weight=2)
        button_frame.rowconfigure(3, weight=3)
        button_frame.rowconfigure(4, weight=1)

        data = self.find_info(self.selected_symbol)

        label_amount_info = ctk.CTkLabel(button_frame,
                                         text="Ilość wszystkich symboli z tego rodzaju: " + str(data['amount']),
                                         corner_radius=5, fg_color='light blue', text_color="black")
        label_amount_info.grid(row=0, column=0, sticky='nsew')

        script_frame = ctk.CTkFrame(button_frame)
        script_frame.grid(row=1, column=0)

        drop_label = ctk.CTkLabel(script_frame, text="Wybierz powiązany skrypt: ")
        drop_label.pack()

        refresh_button = ctk.CTkButton(button_frame, text="Odśwież", command=self.refresh)
        refresh_button.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        scripts = self.find_all_scripts()
        drop = ctk.CTkOptionMenu(master=script_frame, values=scripts, height=40, width=200,
                                 command=lambda choice: change_script(choice))

        script_name = self.find_info(self.selected_symbol)['script']

        if script_name in scripts:
            drop.set(script_name)
        else:
            change_script("default.py")
            drop.set("default.py")

        drop.pack()

        add_symbol_button = ctk.CTkButton(button_frame, text="Dodaj więcej symboli"
                                          , command=self.add_more_symbols)
        add_symbol_button.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)

        delete_button = ctk.CTkButton(button_frame, text="Usuń symbol", fg_color="red",
                                      command=self.delete_symbol)
        delete_button.grid(row=4, column=0, sticky="nsew", padx=10, pady=10)

    def find_all_scripts(self):

        directory = "../data/scripts"

        if os.path.isdir(directory):
            return os.listdir(directory)

        else:
            return []

    def find_info(self, symbol_name):

        with open(self.directory_with_info + "/" + symbol_name + ".json", 'r') as file:
            data = json.load(file)

        return data

    def add_more_symbols(self):

        paint_gui = PaintGUI(self.selected_symbol)
        paint_gui.start()

    def delete_symbol(self):

        os.remove(self.directory + "/" + self.selected_symbol + ".pkl")
        os.remove(self.directory_with_info + "/" + self.selected_symbol + ".json")

        if os.path.exists(self.directory_with_images + "/" + self.selected_symbol + ".png"):
            os.remove(self.directory_with_images + "/" + self.selected_symbol + ".png")

        self.refresh()

    def add_new_symbol(self):

        top_level_add_symbol = ctk.CTkToplevel(self.root)
        top_level_add_symbol.title("Nowy Skrypt")
        top_level_add_symbol.geometry("400x150")

        self.root.eval(f'tk::PlaceWindow {str(top_level_add_symbol)} center')

        label_script_name = ctk.CTkLabel(top_level_add_symbol, text="Nazwa Symbolu:")
        label_script_name.pack(padx=10, pady=10)

        entry_script_name = ctk.CTkEntry(top_level_add_symbol, placeholder_text="np. kolko")
        entry_script_name.pack(padx=10, pady=10)

        entry_script_name.bind("<Return>", lambda event, window=top_level_add_symbol: create_new_symbol(event, window))

        top_level_add_symbol.attributes('-topmost', 'true')

        def create_new_symbol(event, window: ctk.CTkToplevel):
            symbol_name = event.widget.get()

            with open(self.directory + "/" + symbol_name + ".pkl", "wb") as f:
                pickle.dump([], f)

            with open(self.directory_with_info + "/" + symbol_name + ".json", "w") as f:
                json.dump({
                    "amount": 0,
                    "script": "default.py"
                }, f)

            self.refresh()
            window.destroy()

    def switch_symbol(self, clicked_symbol):

        self.selected_symbol = clicked_symbol

        self.clear_bottom_content()
        self.set_bottom_content()
        self.bottom_content.pack(fill='both', expand=True, padx=10, pady=10)

    def refresh(self):

        self.find_all_symbols()
        self.selected_symbol = self.symbols[0]

        self.clear_top_content()
        self.set_top_content()
        self.top_content.pack(fill='both', expand=True, padx=10, pady=10)

        self.clear_bottom_content()
        self.set_bottom_content()
        self.bottom_content.pack(fill='both', expand=True, padx=10, pady=10)

    def enable(self):

        self.top_content.pack(fill='both', expand=True, padx=10, pady=10)
        self.bottom_content.pack(fill='both', expand=True, padx=10, pady=10)

    def unable(self):

        self.top_content.pack_forget()
        self.bottom_content.pack_forget()
