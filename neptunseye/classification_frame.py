import threading
from tkinter import filedialog

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from las_handler import *
from resources.fonts import *
from classification_utils import ClassificationUtils


class ClassificationFrame(ctk.CTkFrame):
    __file_path: str
    __las_handler: LasHandler
    __classification_stride: int

    frame_lb: ctk.CTkLabel
    model_lb: ctk.CTkLabel
    manage_output_lb: ctk.CTkLabel
    model_cbox: ctk.CTkComboBox
    stride_ckb: ctk.CTkCheckBox
    classification_btn: ctk.CTkButton
    save_btn: ctk.CTkButton
    save_as_btn: ctk.CTkButton

    def __init__(self, master, las_handler: LasHandler, **kwargs):
        super().__init__(master, **kwargs)

        self.MODELS = {
            "ExtraTreesClassifier": r"./neptunseye/resources/models/aha41.joblib",
            "ExtraTreesClassifier851": r"./neptunseye/resources/models/ExtraTreesClassifier851.joblib"
        }

        self.selected_model = ctk.StringVar(value="ExtraTreesClassifier")

        self.__las_handler = las_handler
        self.__master = master
        self.use_stride = ctk.BooleanVar(value=False)

        self.set_frame_grid(6, 10)

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
                                     text="Classification options",
                                     font=FONT_HELV_MEDIUM_B,
                                     anchor='center',
                                     justify='center')
        self.manage_output_lb = ctk.CTkLabel(self,
                                             text="Manage output",
                                             font=FONT_HELV_SMALL_B)
        self.classification_btn = ctk.CTkButton(self,
                                                text="Run classification",
                                                command=self.classification_event)
        self.save_btn = ctk.CTkButton(self,
                                      text="Save",
                                      command=self.overwrite_las_file)
        self.save_as_btn = ctk.CTkButton(self,
                                         text="Save as...",
                                         command=self.save_as_las_file)
        self.model_lb = ctk.CTkLabel(self,
                                     text="Select model",
                                     font=FONT_HELV_SMALL_B)
        self.model_cbox = ctk.CTkComboBox(self,
                                          values=list(self.MODELS.keys()),
                                          variable=self.selected_model)
        self.stride_ckb = ctk.CTkCheckBox(self,
                                          text="Use stride",
                                          variable=self.use_stride)

    def set_widgets_positioning(self) -> None:
        """
        Sets the grid positioning for all the widgets in the GUI.

        This function arranges widgets within the GUI using the tkinter grid geometry manager.
        It defines the row, column, columnspan, and sticky options for each widget to achieve the desired layout.

        Returns:
            None
        """
        self.frame_lb.grid(row=0, column=0, columnspan=7, pady=0, sticky="ew")
        self.model_lb.grid(row=1, column=0, padx=15, sticky="w")
        self.model_cbox.grid(row=2, column=0, columnspan=4, padx=15, sticky="ew")
        self.classification_btn.grid(row=9, column=5)
        self.stride_ckb.grid(row=9, column=4)
        self.manage_output_lb.grid(row=1, column=5, padx=20, sticky="w")
        self.save_btn.grid(row=2, column=5, padx=20, sticky="w")
        self.save_as_btn.grid(row=3, column=5, padx=20, sticky="w")

    def classification_event(self) -> bool:

        if not self.__las_handler.file_loaded:
            CTkMessagebox(title="File not loaded", message="Whoops!\n\n"
                                                           "Load .las file first.", icon="cancel")
            return False

        try:
            CTkMessagebox(title="Classificaiton in progress...",
                          message="Working on it!\n\n"
                                  "Please be patient! Classificaiton can take a while depending on"
                                  " the number of points and the speed of your computer.\n\n",
                          icon="info")

            self.classification_btn.configure(state=ctk.DISABLED)
            threading.Thread(target=self.run_classification).start()
        except Exception as e:
            self.classification_btn.configure(state=ctk.NORMAL)
            CTkMessagebox(title="Error", message="That's not good!\n\n"
                                                 "Classification failed!\n\n"
                                                 f"{str(e)}", icon="cancel")
        return True

    def run_classification(self):
        print("Loading model from", self.MODELS[self.selected_model.get()])
        model = ClassificationUtils.load_joblib(self.MODELS[self.selected_model.get()])

        if self.use_stride.get():
            self.classification_stride = self.get_classification_stride()
            X, _ = ClassificationUtils.prepare_data_prediction(
                self.las_handler.data_frame[::self.classification_stride])
            prediction = model.predict(X)
            prediction_fixed = ClassificationFrame.fix_prediction(prediction, self.classification_stride)
            if len(prediction_fixed) != len(self.las_handler.data_frame['classification']):
                prediction_fixed = prediction_fixed[:len(self.las_handler.data_frame['classification'])]
            self.las_handler.data_frame['classification'] = prediction_fixed

        else:
            X, _ = ClassificationUtils.prepare_data_prediction(self.las_handler.data_frame)
            prediction = model.predict(X)
            self.las_handler.data_frame['classification'] = prediction

        self.classification_btn.configure(state=ctk.NORMAL)
        CTkMessagebox(title="Classification completed", message=f"All done!\n\n Classification completed.",
                      icon="check", option_1="OK")
        self.__master.invoke_update_file_description()

    def get_classification_stride(self) -> int:
        return self.__master.get_stride()

    def overwrite_las_file(self) -> None:
        msg = CTkMessagebox(title="Save output",
                            message=f"Are you sure you want to overwrite currently loaded file?\n\n"
                                    f"This operation cannot be undone.\n\n",
                            icon="question", option_1="No", option_2="Yes")
        if msg.get() == "Yes":
            self.las_handler.save_las_file()

    def save_as_las_file(self) -> None:

        file_name = ClassificationFrame.open_save_as_dialog()

        self.las_handler.save_las_file(file_name)

    @staticmethod
    def open_save_as_dialog() -> str:
        filetypes = (
            ("Lidar point cloud data", "*.las"),
            ("All files", "*.*")
        )

        file_path = filedialog.asksaveasfilename(title="Save as...", filetypes=filetypes, defaultextension=".las")
        if file_path and not file_path.endswith(".las"):
            file_path += ".las"

        return file_path
    @staticmethod
    def fix_prediction(prediction, stride):
        new_values = [0] * (len(prediction) * stride)
        for i, val in enumerate(prediction):
            new_index = i * stride
            new_values[new_index] = val
        return new_values

    @property
    def las_handler(self) -> LasHandler:
        return self.__las_handler

    @las_handler.setter
    def las_handler(self, value: LasHandler) -> None:
        self.__las_handler = value

    @property
    def classification_stride(self) -> int:
        return self.__classification_stride

    @classification_stride.setter
    def classification_stride(self, value: int) -> None:
        self.__classification_stride = value