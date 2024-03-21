from tkinter import filedialog

import customtkinter
from CTkMessagebox import CTkMessagebox

from las_handler import *
from resources.fonts import *


class ImportFileFrame(customtkinter.CTkFrame):

    __file_path: str
    __las_handler: LasHandler

    def __init__(self, master, las_handler: LasHandler, **kwargs):
        super().__init__(master, **kwargs)

        self.__las_handler = las_handler

        self.grid_rowconfigure((1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)

        self.grid_columnconfigure((1, 2, 3, 4, 5, 6), weight=1)

        self.frame_label = customtkinter.CTkLabel(self, text="Select and load LAS file", font=FONT_HELV_MEDIUM_B,
                                                  anchor='center', justify='center')
        self.data_desc_label_title = customtkinter.CTkLabel(self, text="Loaded point cloud information", anchor="center",
                                                            justify="center",
                                                            font=FONT_HELV_MEDIUM_B)
        self.data_desc_label1 = customtkinter.CTkLabel(self, text="> " + "Loaded points: ", anchor="w",
                                                       font=FONT_HELV_SMALL_B)
        self.data_desc_label2 = customtkinter.CTkLabel(self, text="> " + "File creation date: ", anchor="w",
                                                       font=FONT_HELV_SMALL_B)
        self.data_desc_label3 = customtkinter.CTkLabel(self, text="> " + "Number of classes: ", anchor="w",
                                                       font=FONT_HELV_SMALL_B)
        self.data_desc_label_v1 = customtkinter.CTkLabel(self, text="-", anchor="w",
                                                         font=FONT_HELV_SMALL)
        self.data_desc_label_v2 = customtkinter.CTkLabel(self, text="-", anchor="w",
                                                         font=FONT_HELV_SMALL)
        self.data_desc_label_v3 = customtkinter.CTkLabel(self, text="-", anchor="w",
                                                         font=FONT_HELV_SMALL)

        self.path_text_box = customtkinter.CTkTextbox(self, height=10, text_color='gray')
        self.path_text_box.configure(state=customtkinter.DISABLED)
        self.button = customtkinter.CTkButton(self, text="Select file", command=self.open_file_dialog)

        # Positioning
        self.frame_label.grid(row=0, column=0, columnspan=7, sticky="ew")
        self.path_text_box.grid(row=1, column=0, columnspan=4, padx=10, sticky="ew")
        self.button.grid(row=1, column=4, padx=5, sticky="w")

        self.data_desc_label_title.grid(row=2, column=0, padx=20, pady=15)
        self.data_desc_label1.grid(row=3, column=0, sticky="W", padx=10)
        self.data_desc_label2.grid(row=4, column=0, sticky="W", padx=10)
        self.data_desc_label3.grid(row=5, column=0, sticky="W", padx=10)
        self.data_desc_label_v1.grid(row=3, column=1, columnspan=3, sticky="W")
        self.data_desc_label_v2.grid(row=4, column=1, columnspan=3, sticky="W")
        self.data_desc_label_v3.grid(row=5, column=1, columnspan=3, sticky="W")

    def open_file_dialog(self) -> None:
        filetypes = (
            ('Lidar point cloud data', '*.las'),
            ('All files', '*.*')
        )

        __file_path = filedialog.askopenfilename(title="Select file", filetypes=filetypes)
        self.__file_path = __file_path
        if __file_path != "":
            self.path_text_box.configure(state=customtkinter.NORMAL)
            self.path_text_box.delete("0.0", "end")
            self.path_text_box.insert("0.0", __file_path)
            self.path_text_box.configure(state=customtkinter.DISABLED)

            self.load_file()

    def load_file(self) -> None:

        temp_las_handler = LasHandler(self.__file_path)

        if temp_las_handler.exception is None:
            self.las_handler.las = temp_las_handler.las
            self.las_handler.data_frame = temp_las_handler.create_dataframe()
            self.las_handler.file_loaded = True

            formatted_points_loaded = f"{self.__las_handler.las.header.point_count:,}".replace(',', ' ')

            CTkMessagebox(title="File loaded", message=f"{formatted_points_loaded} points loaded!",
                          icon="check", option_1="OK")
            self.data_update()
        else:
            CTkMessagebox(title="Failed to load the file",
                          message=f"Oh, snap!\n\nLooks like the file\n\n"
                                  f"\"{self.__file_path}\"\n\n"
                                  f"is not a valid .las file or cannot be loaded!\n\n"
                                  f"Description: {temp_las_handler.exception}",
                          icon="cancel", option_1="OK", sound=True)

    def data_update(self) -> None:

        formatted_points_loaded = f"{self.__las_handler.las.header.point_count:,}".replace(',', ' ')

        self.data_desc_label_v1.configure(text=formatted_points_loaded)
        self.data_desc_label_v2.configure(text=self.las_handler.las.header.creation_date)
        unique_classes_count = len(self.las_handler.unique_classes)
        if unique_classes_count <= 1 and (self.las_handler.unique_classes[0] == 0 or self.las_handler.unique_classes[0] == 1):
            self.data_desc_label_v3.configure(text="Not classified")
        else:
            self.data_desc_label_v3.configure(text=unique_classes_count)

    @property
    def las_handler(self) -> LasHandler:
        return self.__las_handler

    @las_handler.setter
    def las_handler(self, las_handler: LasHandler) -> None:
        self.__las_handler = las_handler
