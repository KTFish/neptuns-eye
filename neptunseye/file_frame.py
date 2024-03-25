from tkinter import filedialog

import customtkinter
from CTkMessagebox import CTkMessagebox

from las_handler import *
from resources.fonts import *


class FileFrame(customtkinter.CTkFrame):
    __file_path: str
    __las_handler: LasHandler

    # Widget definitions
    # TODO: Comment every widgets' placement and function
    frame_lb: customtkinter.CTkLabel
    file_description_lb: customtkinter.CTkLabel
    desc_points_count_lb: customtkinter.CTkLabel
    desc_file_created_lb: customtkinter.CTkLabel
    desc_classes_count_lb: customtkinter.CTkLabel
    desc_points_count_val_lb: customtkinter.CTkLabel
    desc_file_created_val_lb: customtkinter.CTkLabel
    desc_classes_count_val_lb: customtkinter.CTkLabel
    file_path_tbox: customtkinter.CTkTextbox
    import_file_btn: customtkinter.CTkButton

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
        self.frame_lb = customtkinter.CTkLabel(self, text="Select and load LAS file", font=FONT_HELV_MEDIUM_B,
                                               anchor='center', justify='center')
        self.file_description_lb = customtkinter.CTkLabel(self, text="Loaded point cloud information", anchor="center",
                                                          justify="center",
                                                          font=FONT_HELV_MEDIUM_B)
        self.desc_points_count_lb = customtkinter.CTkLabel(self, text="Loaded points: ", anchor="w",
                                                           font=FONT_HELV_SMALL_B)
        self.desc_file_created_lb = customtkinter.CTkLabel(self, text="File creation date: ", anchor="w",
                                                           font=FONT_HELV_SMALL_B)
        self.desc_classes_count_lb = customtkinter.CTkLabel(self, text="Number of classes: ", anchor="w",
                                                            font=FONT_HELV_SMALL_B)
        self.desc_points_count_val_lb = customtkinter.CTkLabel(self, text="-", anchor="w",
                                                               font=FONT_HELV_SMALL)
        self.desc_file_created_val_lb = customtkinter.CTkLabel(self, text="-", anchor="w",
                                                               font=FONT_HELV_SMALL)
        self.desc_classes_count_val_lb = customtkinter.CTkLabel(self, text="-", anchor="w",
                                                                font=FONT_HELV_SMALL)

        self.file_path_tbox = customtkinter.CTkTextbox(self, height=10, text_color='gray')
        self.file_path_tbox.configure(state=customtkinter.DISABLED)
        self.import_file_btn = customtkinter.CTkButton(self, text="Select file", command=self.open_file_dialog)

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
        self.desc_points_count_lb.grid(row=3, column=0, sticky="w", padx=10)
        self.desc_file_created_lb.grid(row=4, column=0, sticky="w", padx=10)
        self.desc_classes_count_lb.grid(row=5, column=0, sticky="w", padx=10)
        self.desc_points_count_val_lb.grid(row=3, column=1, columnspan=3, sticky="w")
        self.desc_file_created_val_lb.grid(row=4, column=1, columnspan=3, sticky="w")
        self.desc_classes_count_val_lb.grid(row=5, column=1, columnspan=3, sticky="w")

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
        temp_las_handler = LasHandler(self.file_path)

        if temp_las_handler.exception is None:
            self.las_handler.las = temp_las_handler.las
            self.las_handler.data_frame = temp_las_handler.create_dataframe()
            self.las_handler.file_loaded = True

            formatted_points_loaded = f"{self.las_handler.las.header.point_count:,}".replace(',', ' ')

            CTkMessagebox(title="File loaded", message=f"{formatted_points_loaded} points loaded!",
                          icon="check", option_1="OK")
            self.update_file_description()
        else:
            CTkMessagebox(title="Failed to load the file",
                          message=f"Oh, snap!\n\nLooks like the file\n\n"
                                  f"\"{self.file_path}\"\n\n"
                                  f"is not a valid .las file or cannot be loaded!\n\n"
                                  f"Description: {temp_las_handler.exception}",
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
            self.file_path_tbox.configure(state=customtkinter.NORMAL)
            self.file_path_tbox.delete("0.0", "end")
            self.file_path_tbox.insert("0.0", path)
            self.file_path_tbox.configure(state=customtkinter.DISABLED)

    def update_file_description(self) -> None:
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

        self.__master.invoke_update_loaded_points_count_lb()

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
