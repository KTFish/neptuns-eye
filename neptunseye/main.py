import configparser, json, os
from typing import Dict, Any

import customtkinter as ctk
from CTkMenuBar import *
from CTkMessagebox import *

from classification_frame import ClassificationFrame
from file_frame import FileFrame
from log_frame import LogFrame
from las_handler import *
from locales import locales
from visualisation_frame import VisualisationFrame

import constants, os_utils

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme(os_utils.resource_path(constants.THEME_FILE_PATH))


class App(ctk.CTk):
    __language = locales.Language.English.value
    __localization_file: Dict
    __file_path: str
    __las_handler: LasHandler

    visualisation_frame: VisualisationFrame
    classification_frame: ClassificationFrame
    log_frame: LogFrame
    file_frame: FileFrame

    def __init__(self) -> None:
        super().__init__()

        self.__file_path = None
        self.__las_handler = LasHandler()
        self.CFG_PATH = os_utils.resource_path(constants.CONFIG_FILE_PATH)

        language = App.get_language(self.CFG_PATH)
        if language == "Polski":
            self.language = locales.Language.Polish.value
        else:
            self.language = locales.Language.English.value

        self.load_localization_file()
        self.strings = self.localization_file

        # Window setup
        self.title(f"Neptun's Eye v{constants.APP_VERSION}")

        toolbar_menu = CTkTitleMenu(master=self)
        settings_tbmbtn = toolbar_menu.add_cascade("⚒ | " + self.localization_file["gui"]["toolbar"]["settings_btn"],
                                                   command=self.open_notepad_config)
        language_tbmbtn = toolbar_menu.add_cascade("🏴 | " + self.localization_file["gui"]["toolbar"]["language_btn"])
        dropdown = CustomDropdownMenu(widget=language_tbmbtn)
        dropdown.add_option(option="English", command=lambda: App.set_language(self.CFG_PATH, "English"))
        dropdown.add_option(option="Polski", command=lambda: App.set_language(self.CFG_PATH, "Polski"))

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.width = int(screen_width * 0.65)
        self.height = int(screen_height * 0.45)
        self.maxw = int(screen_width * 0.8)
        self.maxh = int(screen_height * 0.6)
        self.geometry(f"{self.width}x{self.height}")
        self.minsize(self.width, self.height)
        self.maxsize(self.maxw, self.maxh)
        self.resizable(True, True)
        self.after(201, lambda: self.iconbitmap(os_utils.resource_path(constants.APP_ICON_PATH)))

        self.initialize_frames()

        self.invoke_insert_text(f"Neptun's Eye v{constants.APP_VERSION} - Welcome!\n"
                                f"===============================")
        self.invoke_insert_text("Event log feature is in \"Work in progress\" state."
                                "\nNot all events are logged yet.")
        self.invoke_insert_text_with_timestamp("Ready. Please load the file.")

    def initialize_frames(self) -> None:
        """
        Initialize frames within the application window.

        Configures grid row and column weights to allow frames to resize properly.
        Creates and places three frames within the application window.

        Returns:
            None
        """
        self.grid_rowconfigure((0, 1), weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        self.file_frame = FileFrame(master=self,
                                    las_handler=self.__las_handler,
                                    locales=self.localization_file)
        self.file_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.visualisation_frame = VisualisationFrame(master=self,
                                                      las_handler=self.__las_handler,
                                                      locales=self.localization_file)
        self.visualisation_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        self.classification_frame = ClassificationFrame(master=self,
                                                        las_handler=self.__las_handler,
                                                        locales=self.localization_file)
        self.classification_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.log_frame = LogFrame(master=self,
                                  las_handler=self.__las_handler,
                                  locales=self.localization_file)
        self.log_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

    def load_localization_file(self) -> None:
        """Loads and sets the localization."""
        with open(os_utils.resource_path(f"locales\\localization_{self.language}.json"), 'r', encoding='utf-8') as file:
            self.localization_file = json.load(file)

    def invoke_update_loaded_points_count_lb(self) -> None:
        self.visualisation_frame.update_generated_points_count_lb()

    def invoke_update_file_description(self) -> None:
        self.file_frame.update_file_description(after_classification=True)

    def invoke_insert_text_with_timestamp(self, text: str) -> None:
        self.log_frame.insert_text_with_timestamp(text)

    def invoke_insert_text(self, text: str) -> None:
        self.log_frame.insert_text(text)

    def get_stride(self) -> int:
        return self.visualisation_frame.rendering_stride

    def open_notepad_config(self) -> None:
        os.system(f'notepad.exe {os_utils.resource_path(self.CFG_PATH)}')

    @staticmethod
    def set_language(file_path, new_language):
        """
        Set the language in the configuration file and prompt the user to restart the application.

        Args:
            file_path (str): The path to the configuration file.
            new_language (str): The new language to be set in the configuration file.
        """

        config = configparser.ConfigParser()
        config.read(file_path)
        config['Settings']['language'] = f'"{new_language}"'

        if new_language == "Polski":
            CTkMessagebox(title="Zmiana języka", message="Aby zmienić język, uruchom aplikację ponownie.",
                          icon="info")
        else:
            CTkMessagebox(title="Change language", message="To change the language restart the app.",
                          icon="info")

        try:
            with open(file_path, 'w') as configfile:
                config.write(configfile)
        except Exception as e:
            CTkMessagebox(title="Error", message="Could not load config.ini file.\n Language will be set to English.\n"
                                                 f"Visualisation with pptk will not work.{e}",
                          icon="cancel")

    @staticmethod
    def get_language(file_path) -> str:
        return os_utils.get_config(file_path, 'Settings', 'language')

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
