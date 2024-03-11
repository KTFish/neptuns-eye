import tkinter
import customtkinter
from tkinter import filedialog
import json
from typing import Dict, Any
import locales.locales as locales
from import_file_frame import *

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

class SettingsFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.label = customtkinter.CTkLabel(self, text="abc")
        self.label.grid(row=0, column=0, padx=20)

class App(customtkinter.CTk):

    __language = locales.Language.English
    __localization_file: Dict
    __file_path: str

    APP_ICON_PATH = "resources\\neptuns-eye-logo.ico"

    def __init__(self) -> None:
        super().__init__()

        __file_path = None

        # Window setup
        self.title("Neptun's Eye v0.1")
        self.width = int(self.winfo_screenwidth() / 2.5)
        self.height = int(self.winfo_screenheight() / 2)
        self.geometry(f"{self.width}x{self.height}")
        self.minsize(500, 500)
        self.after(201, lambda: self.iconbitmap(self.APP_ICON_PATH))

        # Frames setup
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.my_frame = ImportFileFrame(master=self, filepath=__file_path)
        self.my_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.my_frame = SettingsFrame(master=self)
        self.my_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

    def load_localization_file(self) -> None:
        """Loads and sets the localization."""
        with open(f"localization_{self.language.value}.json", 'r', encoding='utf-8') as file:
            self.localization_file = json.load(file)

    @property
    def localization_file(self) -> Dict:
        return self.__localization_file

    @property
    def language(self) -> str:
        return self.__language

    @localization_file.setter
    def localization_file(self, path: Dict) -> None:
        self.__localization_file = path

    @language.setter
    def language(self, lang_str: Any) -> None:
        self.__language = lang_str


if __name__ == "__main__":
    app = App()
    app.mainloop()
