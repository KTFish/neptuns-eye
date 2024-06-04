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
import os_utils
import sklearn
import sklearn.ensemble._forest


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

    def __init__(self, master, las_handler: LasHandler, locales: Dict, **kwargs):
        super().__init__(master, **kwargs)

        self.strings = locales

        with open(os_utils.resource_path(constants.MODELS_DEFINITION_FILE_PATH), 'r') as file:
            try:
                self.models: Dict[str, str] = json.load(file)
            except Exception as e:
                CTkMessagebox(title="Error",
                              message=self.strings["messages"]["models_file_err_msg"].format(e=str(e)),
                              icon="cancel")

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
                                     text=self.strings["gui"]["classification_frame"]["header_lb"],
                                     font=FONT_HELV_MEDIUM_B,
                                     anchor='center',
                                     justify='center')
        self.manage_output_lb = ctk.CTkLabel(self,
                                             text=self.strings["gui"]["classification_frame"]["manage_output"],
                                             font=FONT_HELV_SMALL_B)
        self.classification_btn = ctk.CTkButton(self,
                                                text=self.strings["gui"]["classification_frame"][
                                                    "run_classification_btn"],
                                                command=self.classification_event)
        self.save_btn = ctk.CTkButton(self,
                                      text=self.strings["gui"]["classification_frame"]["save_output_btn"],
                                      command=self.overwrite_las_file)
        self.save_as_btn = ctk.CTkButton(self,
                                         text=self.strings["gui"]["classification_frame"]["save_as_output_btn"],
                                         command=self.save_as_las_file)
        self.model_lb = ctk.CTkLabel(self,
                                     text="",
                                     font=FONT_HELV_SMALL_B)
        self.model_cbox = ctk.CTkComboBox(self,
                                          values=list(self.models.keys()),
                                          variable=self.selected_model)
        self.stride_ckb = ctk.CTkCheckBox(self,
                                          text=self.strings["gui"]["classification_frame"]["use_stride_ckb"],
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
        self.model_cbox.grid(row=2, column=0, columnspan=5, padx=15, sticky="we")
        self.classification_btn.grid(row=8, column=5, padx=15, pady=10, sticky='w')
        self.save_btn.grid(row=2, column=5, padx=15, sticky="w")
        self.save_as_btn.grid(row=3, column=5, padx=15, sticky="w")
        self.stride_ckb.grid(row=8, column=4, pady=10)
        self.manage_output_lb.grid(row=1, column=5, padx=20, sticky="w")

    def classification_event(self) -> bool:


        if not self.__las_handler.file_loaded:
            CTkMessagebox(title=self.strings["messages"]["file_not_loaded_err_title"],
                          message=self.strings["messages"]["file_not_loaded_err_msg"], icon="cancel")
            return False

        try:
            CTkMessagebox(title=self.strings["messages"]["classification_in_progress_title"],
                          message=self.strings["messages"]["classification_in_progress_msg"],
                          icon="info")

            self.classification_btn.configure(state=ctk.DISABLED)
            threading.Thread(target=self.run_classification).start()
        except Exception as e:
            self.classification_btn.configure(state=ctk.NORMAL)
            CTkMessagebox(title=self.strings["messages"]["classification_failed_err_title"],
                          message=self.strings["messages"]["classification_failed_err_msg"].format(e=str(e)),
                          icon="cancel")
        return True

    def run_classification(self) -> bool:
        joblib_file_path = os_utils.resource_path(str(self.models[self.selected_model.get()]))
        self.__master.invoke_insert_text_with_timestamp("Loading model from:\n" + joblib_file_path)
        try:
            model = ClassificationUtils.load_joblib(joblib_file_path)
        except FileNotFoundError:
            CTkMessagebox(title=self.strings["messages"]["classification_failed_err_title"],
                          message=self.strings["messages"]["model_not_found_err_msg"].format(
                              model=self.selected_model.get()),
                          icon="cancel")
            self.classification_btn.configure(state=ctk.NORMAL)
            return False
        except Exception as e:
            CTkMessagebox(title=self.strings["messages"]["classification_failed_err_title"],
                          message=self.strings["messages"]["model_loading_err_msg"].format(e=str(e)),
                          icon="cancel")
            self.classification_btn.configure(state=ctk.NORMAL)
            return False

        self.__master.invoke_insert_text_with_timestamp("Model loaded successfully.")
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
            self.__master.invoke_insert_text_with_timestamp("Classification completed.")

        self.classification_btn.configure(state=ctk.NORMAL)
        CTkMessagebox(title=self.strings["messages"]["classification_successful_title"],
                      message=self.strings["messages"]["classification_successful_msg"],
                      icon="check", option_1="OK")
        self.__master.invoke_update_file_description()

        return True

    def get_classification_stride(self) -> int:
        return self.__master.get_stride()

    def overwrite_las_file(self) -> None:
        msg = CTkMessagebox(title=self.strings["messages"]["save_popup_title"],
                            message=self.strings["messages"]["save_popup_message"],
                            icon="question", option_1=self.strings["messages"]["no"],
                            option_2=self.strings["messages"]["yes"])
        if msg.get() == self.strings["messages"]["yes"]:
            self.las_handler.save_las_file()

    def save_as_las_file(self) -> None:

        file_name = ClassificationFrame.open_save_as_dialog()

        self.las_handler.save_las_file(file_name)

    def open_save_as_dialog(self) -> str:
        filetypes = (
            ("Lidar point cloud data", "*.las"),
            ("All files", "*.*")
        )

        file_path = filedialog.asksaveasfilename(
            title=self.strings["gui"]["classification_frame"]["save_as_output_btn"],
            filetypes=filetypes, defaultextension=".las")
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
