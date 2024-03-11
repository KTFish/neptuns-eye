import tkinter
import customtkinter
from tkinter import filedialog
import json
from typing import Dict, Any
from CTkMessagebox import CTkMessagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import locales.locales as locales
from las_handler import *


class VisualisationFrame(customtkinter.CTkFrame):
    __file_path: str
    __las_handler: LasHandler

    def __init__(self, master, las_handler: LasHandler, **kwargs):
        super().__init__(master, **kwargs)

        self.__master = master
        self.__las_handler = las_handler

        self.frame_label = customtkinter.CTkLabel(self, text="Visualisation options")
        self.button = customtkinter.CTkButton(master=self, text="Render 2D", command=self.test)

        # Positioning
        self.frame_label.grid(row=0, column=0)
        self.button.grid(row=1, column=0)

    def test(self) -> bool:
        print(self.__las_handler.file_loaded)
        if self.__las_handler.file_loaded is False:
            CTkMessagebox(title="File not loaded", message="Whoops!\n"
                                                           "Load .las file first.", icon="cancel")
            return False

        try:
            self.__las_handler.visualize_las_2d()
        except Exception as e:
            CTkMessagebox(title="Error", message=str(e), icon="cancel")
            return False

        canvas = FigureCanvasTkAgg(self.__las_handler.visualisation_figure, master=self.__master)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=1)
        print("OK")

        return True