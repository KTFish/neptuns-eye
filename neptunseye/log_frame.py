import json
import threading
from tkinter import filedialog
from typing import Dict

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from las_handler import *
from resources.fonts import *
from classification_utils import ClassificationUtils
import constants


class LogFrame(ctk.CTkFrame):
    __las_handler: LasHandler

    frame_lb: ctk.CTkLabel
    log_tbox: ctk.CTkTextbox

    def __init__(self, master, las_handler: LasHandler, locales: Dict, **kwargs):
        super().__init__(master, **kwargs)

        self.__master = master
        self.configure(fg_color="gray12")

        self.set_frame_grid(1, 6)

        self.initialize_widgets()
        self.set_widgets_positioning()

    def set_frame_grid(self, num_columns: int, num_rows: int) -> None:
        """Sets up the grid layout for the GUI frame.

        This function configures the rows and columns of the main GUI frame using the tkinter grid geometry manager.
        It sets a weight of 1 for all rows and columns, which likely creates a flexible grid that adapts to the
        window size.

        Args:
            num_columns: The number of columns in the grid.
            num_rows: The number of rows in the grid.

        Returns:
            None
        """
        for i in range(num_columns):
            self.grid_columnconfigure(i, weight=1)

        for i in range(num_rows):
            self.grid_rowconfigure(i, weight=1)

    def initialize_widgets(self):
        """Initializes all the widgets used in the GUI.

        This function creates instances of various CustomTkinter widgets
        and configures their basic properties. These widgets represent the
        user interface elements for interacting with the application.

        Returns:
            None
        """
        self.frame_lb = ctk.CTkLabel(self,
                                     text="Event log",
                                     font=FONT_HELV_MEDIUM_B,
                                     anchor='center',
                                     justify='center')

        self.log_tbox = ctk.CTkTextbox(self, bg_color='gray12', fg_color='gray12')

    def set_widgets_positioning(self) -> None:
        """
        Sets the grid positioning for all the widgets in the GUI.

        This function arranges widgets within the GUI using the tkinter grid geometry manager.
        It defines the row, column, columnspan, and sticky options for each widget to achieve the desired layout.

        Returns:
            None
        """
        self.frame_lb.grid(row=0, column=0, columnspan=6, sticky="ew")
        self.log_tbox.grid(row=1, column=0, columnspan=6, sticky="nsew", padx=10)
