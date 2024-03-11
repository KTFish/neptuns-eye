import tkinter
import customtkinter
from tkinter import filedialog
import json
from typing import Dict, Any
from CTkMessagebox import CTkMessagebox
import locales.locales as locales
from las_handler import *


class ImportFileFrame(customtkinter.CTkFrame):

    __file_path: str
    __las_handler: LasHandler

    def __init__(self, master, las_handler: LasHandler, **kwargs):
        super().__init__(master, **kwargs)

        self.__las_handler = las_handler

        self.frame_label = customtkinter.CTkLabel(self, text="Select and load .LAS file")

        self.path_text_box = customtkinter.CTkTextbox(self, height=10, width=400, text_color='gray')
        self.path_text_box.configure(state=customtkinter.DISABLED)
        self.button = customtkinter.CTkButton(master=self, text="Select file", command=self.open_file_dialog)

        # Positioning
        self.path_text_box.grid(row=1, column=0, padx=5)
        self.frame_label.grid(row=0, column=0)
        self.button.grid(row=1, column=1, padx=10)

    def open_file_dialog(self):

        filetypes = (
            ('Lidar point cloud data', '*.las'),
            ('All files', '*.*')
        )

        __file_path = filedialog.askopenfilename(title="Select file", filetypes=filetypes)
        print(__file_path)
        if __file_path != "":
            self.path_text_box.configure(state=customtkinter.NORMAL)
            self.path_text_box.insert("0.0", __file_path)
            self.path_text_box.configure(state=customtkinter.DISABLED)

            temp_las_handler = LasHandler(__file_path)
            self.__las_handler.las = temp_las_handler.las
            self.__las_handler.file_loaded = True

            CTkMessagebox(title="File loaded", message=f"{self.__las_handler.las.header.point_count} points loaded!",
                          icon="check", option_1="OK")

    @property
    def las_handler(self) -> LasHandler:
        return self.__las_handler

    @las_handler.setter
    def las_handler(self, las_handler: LasHandler) -> None:
        self.__las_handler = las_handler
