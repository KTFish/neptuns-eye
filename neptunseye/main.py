import json
from typing import Dict, Any

import customtkinter

from classification_frame import *
from file_frame import *
from las_handler import *
from locales import locales
from visualisation_frame import *

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")


class App(customtkinter.CTk):

    __language = locales.Language.English
    __localization_file: Dict
    __file_path: str
    __las_handler: LasHandler

    visualisation_frame: VisualisationFrame
    classification_frame: ClassificationFrame
    file_frame: FileFrame

    APP_ICON_PATH = r"./neptunseye/resources/neptuns-eye-logo.ico"
    APP_VERSION = "0.1.0"

    def __init__(self) -> None:
        super().__init__()

        self.__file_path = None
        self.__las_handler = LasHandler()

        # Window setup
        self.title(f"Neptun's Eye v{self.APP_VERSION}")
        self.width = int(self.winfo_screenwidth() / 2.5)
        self.height = int(self.winfo_screenheight() / 2)
        self.geometry(f"{self.width}x{self.height}")
        self.minsize(1280, 720)
        self.after(201, lambda: self.iconbitmap(self.APP_ICON_PATH))

        self.initialize_frames()

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

        self.file_frame = FileFrame(master=self, las_handler=self.__las_handler)
        self.file_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.visualisation_frame = VisualisationFrame(master=self, las_handler=self.__las_handler)
        self.visualisation_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

        self.classification_frame = ClassificationFrame(master=self, las_handler=self.__las_handler)
        self.classification_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

    def load_localization_file(self) -> None:
        """Loads and sets the localization."""
        with open(f"localization_{self.language}.json", 'r', encoding='utf-8') as file:
            self.localization_file = json.load(file)

    def invoke_update_loaded_points_count_lb(self) -> None:
        self.visualisation_frame.update_generated_points_count_lb()

    def invoke_update_file_description(self) -> None:
        self.file_frame.update_file_description(after_classification=True)

    def get_stride(self) -> int:
        return self.visualisation_frame.rendering_stride

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
