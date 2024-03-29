import customtkinter

from las_handler import *


class ClassificationFrame(customtkinter.CTkFrame):

    __file_path: str
    __las_handler: LasHandler

    def __init__(self, master, las_handler: LasHandler, **kwargs):
        super().__init__(master, **kwargs)

        self.__las_handler = las_handler

        self.frame_lb = customtkinter.CTkLabel(self, text="This will be a frame with classification options")

        # Positioning
        self.frame_lb.grid(row=0, column=0, padx=10, pady=10)