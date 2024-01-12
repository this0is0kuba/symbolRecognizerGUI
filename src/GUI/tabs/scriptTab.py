import subprocess

import customtkinter as ctk
import os
import math

from sys import platform


class ScriptTab:

    def __init__(self, top_content: ctk.CTkFrame, bottom_content: ctk.CTkFrame, root: ctk.CTk):

        self.root = root
        self.root_top_content = top_content
        self.root_bottom_content = bottom_content

        self.top_content = None
        self.bottom_content = None

        self.directory = "../data/scripts"
        self.scripts = []
        self.find_all_scripts()

        self.selected_script = None
        self.script_text_element: ctk.CTkTextbox | None = None

        if len(self.scripts) > 0:
            self.selected_script = self.scripts[0]

        self.set_top_content()
        self.set_bottom_content()

    def find_all_scripts(self):

        if os.path.isdir(self.directory):
            self.scripts = os.listdir(self.directory)

        else:
            self.scripts = []

    def set_top_content(self):

        self.top_content = ctk.CTkFrame(self.root_top_content)

        for i in range(6):
            self.top_content.columnconfigure(i, weight=1)

        for i in range(math.ceil((len(self.scripts) + 1) / 6)):
            self.top_content.rowconfigure(i, weight=1)

        self.top_content.grid_propagate(False)

        for i, script in enumerate(self.scripts):

            script_button = ctk.CTkButton(self.top_content, text=script,
                                          command=lambda current_script=script: self.switch_script(current_script))
            script_button.grid(row=i//6, column=i % 6, sticky="nsew", padx=10, pady=10)

            if len(self.scripts) < 6:
                script_button.grid(pady=100)

        plus_script_button = ctk.CTkButton(self.top_content, text="+", fg_color="green", command=self.add_script,
                                           hover_color='dark green')
        plus_script_button.grid(row=len(self.scripts)//6, column=len(self.scripts) % 6, sticky="nsew", padx=10, pady=10)

        if len(self.scripts) < 6:
            plus_script_button.grid(pady=100)

    def clear_top_content(self):
        self.top_content.destroy()

    def set_bottom_content(self):

        self.bottom_content = ctk.CTkFrame(self.root_bottom_content)

        self.bottom_content.columnconfigure(0, weight=3)
        self.bottom_content.columnconfigure(1, weight=1)
        self.bottom_content.rowconfigure(0, weight=1)

        self.bottom_content.grid_propagate(False)

        self.set_config_buttons()

        self.script_text_element = ctk.CTkTextbox(self.bottom_content)
        self.display_script(self.selected_script)
        self.script_text_element.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    def display_script(self, script_name):

        if script_name is None:
            script_content = ''
        else:
            file = open(self.directory + "/" + script_name, 'r', encoding='utf-8')
            script_content = file.read()
            file.close()

        self.script_text_element.delete('1.0', ctk.END)
        self.script_text_element.insert(ctk.END, script_content)

    def set_config_buttons(self):

        button_frame = ctk.CTkFrame(self.bottom_content)
        button_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        button_frame.columnconfigure(0, weight=1)
        button_frame.rowconfigure(0, weight=1)
        button_frame.rowconfigure(1, weight=1)
        button_frame.rowconfigure(2, weight=3)
        button_frame.rowconfigure(3, weight=1)

        refresh_button = ctk.CTkButton(button_frame, text="Odśwież", command=self.refresh)
        refresh_button.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        open_in_vscode_button = ctk.CTkButton(button_frame, text="Otwórz w VSCode", command=lambda: open_in_vscode())
        open_in_vscode_button.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        save_changes_button = ctk.CTkButton(button_frame, text="Zapisz zmiany", command=lambda: save_changes())
        save_changes_button.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        delete_button = ctk.CTkButton(button_frame, text="Usuń Skrypt", fg_color="red", hover_color='dark red',
                                      command=lambda: delete_script())
        delete_button.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)

        def open_in_vscode():

            if platform == "win32":
                subprocess.run("code " + self.directory + "/" + self.selected_script, shell=True)

            elif platform == "darwin" or platform == "linux":
                subprocess.run("code " + self.directory + "/" + self.selected_script)


        def save_changes():

            with open(self.directory + "/" + self.selected_script, 'w') as file:
                file.write(self.script_text_element.get("1.0", ctk.END))

        def delete_script():

            if self.selected_script != "default.py":

                os.remove(self.directory + "/" + self.selected_script)
                self.refresh()

    def switch_script(self, clicked_script):

        self.display_script(clicked_script)

        self.selected_script = clicked_script

    def add_script(self):

        top_level_add_script = ctk.CTkToplevel(self.root)
        top_level_add_script.title("Nowy Skrypt")
        top_level_add_script.geometry("400x150")

        self.root.eval(f'tk::PlaceWindow {str(top_level_add_script)} center')

        label_script_name = ctk.CTkLabel(top_level_add_script, text="Nazwa Skryptu:")
        label_script_name.pack(padx=10, pady=10)

        entry_script_name = ctk.CTkEntry(top_level_add_script, placeholder_text="np. moj_skrypt.py")
        entry_script_name.pack(padx=10, pady=10)

        entry_script_name.bind("<Return>", lambda event, window=top_level_add_script: create_script(event, window))

        top_level_add_script.attributes('-topmost', 'true')

        def create_script(event, window: ctk.CTkToplevel):
            script_name = event.widget.get()

            with open(self.directory + "/" + script_name, 'a') as file:
                pass

            self.refresh()
            window.destroy()

    def refresh(self):

        self.find_all_scripts()

        self.selected_script = self.scripts[0]

        self.clear_top_content()
        self.set_top_content()
        self.top_content.pack(fill='both', expand=True, padx=10, pady=10)

        self.display_script(self.scripts[0])

    def enable(self):

        self.top_content.pack(fill='both', expand=True, padx=10, pady=10)
        self.bottom_content.pack(fill='both', expand=True, padx=10, pady=10)

    def unable(self):

        self.top_content.pack_forget()
        self.bottom_content.pack_forget()



