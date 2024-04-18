from tkinter import filedialog

import customtkinter as ctk
import json
from CTkMessagebox import CTkMessagebox

from las_handler import *
from resources.fonts import *


class FileFrame(ctk.CTkFrame):
    __file_path: str
    __las_handler: LasHandler

    CLASSES_DEFINITION_FILE_PATH = r"./neptunseye/config/classes_definition.json"

    # Widget definitions
    frame_lb: ctk.CTkLabel
    file_description_lb: ctk.CTkLabel
    classification_description_lb: ctk.CTkLabel
    desc_points_count_lb: ctk.CTkLabel
    desc_file_created_lb: ctk.CTkLabel
    desc_classes_count_lb: ctk.CTkLabel
    desc_points_count_val_lb: ctk.CTkLabel
    desc_file_created_val_lb: ctk.CTkLabel
    desc_classes_count_val_lb: ctk.CTkLabel
    file_path_tbox: ctk.CTkTextbox
    desc_classification_tbox: ctk.CTkTextbox
    import_file_btn: ctk.CTkButton

    def __init__(self, master, las_handler: LasHandler, **kwargs):
        super().__init__(master, **kwargs)

        self.las_handler = las_handler
        self.__master = master

        self.set_frame_grid(10, 8)

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
                                     text="Select and load LAS file",
                                     font=FONT_HELV_MEDIUM_B,
                                     anchor='center', justify='center')
        self.classification_description_lb = ctk.CTkLabel(self,
                                                          text="Classification",
                                                          anchor="center",
                                                          justify="center",
                                                          font=FONT_HELV_MEDIUM_B)
        self.file_description_lb = ctk.CTkLabel(self,
                                                text="Loaded point cloud information",
                                                anchor="center",
                                                justify="center",
                                                font=FONT_HELV_MEDIUM_B)
        self.desc_points_count_lb = ctk.CTkLabel(self, text="Loaded points: ",
                                                 anchor="w",
                                                 font=FONT_HELV_SMALL_B)
        self.desc_file_created_lb = ctk.CTkLabel(self, text="File creation date: ",
                                                 anchor="w",
                                                 font=FONT_HELV_SMALL_B)
        self.desc_classes_count_lb = ctk.CTkLabel(self, text="Number of classes: ",
                                                  anchor="w",
                                                  font=FONT_HELV_SMALL_B)
        self.desc_points_count_val_lb = ctk.CTkLabel(self, text="-",
                                                     anchor="w",
                                                     font=FONT_HELV_SMALL)
        self.desc_file_created_val_lb = ctk.CTkLabel(self, text="-",
                                                     anchor="w",
                                                     font=FONT_HELV_SMALL)
        self.desc_classes_count_val_lb = ctk.CTkLabel(self, text="-",
                                                      anchor="w",
                                                      font=FONT_HELV_SMALL)
        self.file_path_tbox = ctk.CTkTextbox(self,
                                             height=10,
                                             text_color='gray')
        self.import_file_btn = ctk.CTkButton(self,
                                             text="Select file",
                                             command=self.open_file_dialog)
        self.desc_classification_tbox = ctk.CTkTextbox(self)
        self.file_path_tbox.configure(state=ctk.DISABLED)
        self.desc_classification_tbox.insert("0.0", "[File not loaded]")
        self.desc_classification_tbox.configure(state=ctk.DISABLED)

    def set_widgets_positioning(self) -> None:
        """
        Sets the grid positioning for all the widgets in the GUI.

        This function arranges widgets within the GUI using the tkinter grid geometry manager.
        It defines the row, column, columnspan, and sticky options for each widget to achieve the desired layout.

        Returns:
            None
        """
        self.frame_lb.grid(row=0, column=0, columnspan=7, sticky="ew")
        self.file_path_tbox.grid(row=1, column=0, columnspan=4, padx=10, sticky="ew")
        self.import_file_btn.grid(row=1, column=4, padx=5, sticky="w")

        self.file_description_lb.grid(row=2, column=0, padx=20, pady=10)
        self.classification_description_lb.grid(row=2, column=5)
        self.desc_points_count_lb.grid(row=3, column=0, sticky="w", padx=10)
        self.desc_file_created_lb.grid(row=4, column=0, sticky="w", padx=10)
        self.desc_classes_count_lb.grid(row=5, column=0, sticky="w", padx=10)
        self.desc_points_count_val_lb.grid(row=3, column=1, columnspan=4, sticky="w")
        self.desc_file_created_val_lb.grid(row=4, column=1, columnspan=4, sticky="w")
        self.desc_classes_count_val_lb.grid(row=5, column=1, columnspan=4, sticky="w")
        self.desc_classification_tbox.grid(row=3, column=5, columnspan=5, rowspan=5, sticky="nswe", padx=20, pady=20)

    def open_file_dialog(self) -> None:
        """
        Open a file dialog to select a LAS file.

        Displays a file dialog window allowing the user to select a LAS file (.las extension).
        After selecting a file, updates the application's internal file path.
        Then, triggers the 'load_file' method to load the selected file into the application.

        Returns:
            None
        """
        filetypes = (
            ("Lidar point cloud data", "*.las"),
            ("All files", "*.*")
        )

        file_path = filedialog.askopenfilename(title="Select file", filetypes=filetypes)

        self.file_path = file_path
        self.update_file_path_tbox(file_path)

        self.load_file()

    def load_file(self) -> None:
        """
        Load a LAS file into the application.

        Loads a LAS file using the provided file path. If successful, updates the
        application's internal state with the loaded data and displays a success message.
        If loading fails, displays an error message.

        Returns:
            None
        """
        try:
            temp_las_handler = LasHandler(self.file_path)

            self.las_handler.las = temp_las_handler.las
            self.las_handler.data_frame = temp_las_handler.create_dataframe()
            self.las_handler.file_loaded = True

            formatted_points_loaded = f"{self.las_handler.las.header.point_count:,}".replace(',', ' ')

            CTkMessagebox(title="File loaded", message=f"{formatted_points_loaded} points loaded!",
                          icon="check", option_1="OK")
            self.update_file_description()
        except Exception as e:
            if temp_las_handler.exception is not None:
                e = temp_las_handler.exception
            CTkMessagebox(title="Failed to load the file",
                          message=f"Oh, snap!\n\nLooks like the file\n\n"
                                  f"\"{self.file_path}\"\n\n"
                                  f"is not a valid .las file or cannot be loaded!\n\n"
                                  f"Description: {e}",
                          icon="cancel", option_1="OK", sound=True)

    def update_file_path_tbox(self, path: str) -> None:
        """
        Update the file path display widget with the given path.

        Args:
            path (str): The file path to display in the widget.

        Returns:
            None
        """
        if path != '':
            self.file_path_tbox.configure(state=ctk.NORMAL)
            self.file_path_tbox.delete("0.0", "end")
            self.file_path_tbox.insert("0.0", path)
            self.file_path_tbox.configure(state=ctk.DISABLED)

    def update_file_description(self, after_classification: bool = False) -> None:
        """
        Update the file description labels with information from the loaded LAS file.

        Returns:
            None
        """
        formatted_points_loaded = f"{self.las_handler.las.header.point_count:,}".replace(',', ' ')

        self.desc_points_count_val_lb.configure(text=formatted_points_loaded)
        self.desc_file_created_val_lb.configure(text=self.las_handler.las.header.creation_date)

        unique_classes_count = len(self.las_handler.unique_classes)
        if unique_classes_count <= 1 and (
                self.las_handler.unique_classes[0] == 0 or self.las_handler.unique_classes[0] == 1):
            self.desc_classes_count_val_lb.configure(text="Not classified")
        else:
            self.desc_classes_count_val_lb.configure(text=unique_classes_count)

        self.__update_desc_classification_tbox()

        self.__master.invoke_update_loaded_points_count_lb()

    def __update_desc_classification_tbox(self) -> None:
        self.desc_classification_tbox.configure(state=ctk.NORMAL)
        self.desc_classification_tbox.delete("0.0", "end")
        for class_id in sorted(self.las_handler.unique_classes):

            with open(self.CLASSES_DEFINITION_FILE_PATH, 'r') as file:

                class_definitions = json.load(file)

            class_definitions = {int(key): value for key, value in class_definitions.items()}
            class_definitions_keys = list(class_definitions.keys())

            if class_definitions is not None:
                if class_id in class_definitions_keys:
                    self.desc_classification_tbox.insert("end", f"[{int(class_id)}]:  "
                                                                f"{class_definitions[int(class_id)]}\n")
                else:
                    self.desc_classification_tbox.insert("end", f"{int(class_id)}: Undefined\n")
        self.desc_classification_tbox.configure(state=ctk.DISABLED)

    @property
    def las_handler(self) -> LasHandler:
        return self.__las_handler

    @property
    def file_path(self) -> str:
        return self.__file_path

    @las_handler.setter
    def las_handler(self, las_handler: LasHandler) -> None:
        self.__las_handler = las_handler

    @file_path.setter
    def file_path(self, value: str) -> None:
        self.__file_path = value
