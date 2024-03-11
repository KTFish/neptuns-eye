import tkinter
import customtkinter
from tkinter import filedialog
import json
from typing import Dict, Any
from CTkMessagebox import CTkMessagebox
import locales.locales as locales
from las_handler import *


class ClassificationFrame(customtkinter.CTkFrame):

    __file_path: str
    __las_handler: LasHandler

    def __init__(self, master, las_handler: LasHandler, **kwargs):
        super().__init__(master, **kwargs)

        self.__las_handler = las_handler

        self.frame_label = customtkinter.CTkLabel(self, text="This will be a frame with classification options")

        # Positioning
        self.frame_label.grid(row=0, column=0)