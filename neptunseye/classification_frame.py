import threading

import customtkinter
from CTkMessagebox import CTkMessagebox

from las_handler import *
from resources.fonts import *
from classification_utils import ClassificationUtils


class ClassificationFrame(customtkinter.CTkFrame):
    __file_path: str
    __las_handler: LasHandler
    __classification_stride: int

    frame_lb: customtkinter.CTkLabel
    model_lb: customtkinter.CTkLabel
    model_cbox: customtkinter.CTkComboBox
    stride_ckb: customtkinter.CTkCheckBox
    classification_btn: customtkinter.CTkButton

    def __init__(self, master, las_handler: LasHandler, **kwargs):
        super().__init__(master, **kwargs)

        self.MODELS = {
            "ExtraTreesClassifier": "resources\\models\\aha41.joblib"
        }

        self.selected_model = "ExtraTreesClassifier"

        self.__las_handler = las_handler
        self.__master = master
        self.use_stride = customtkinter.BooleanVar(value=False)

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
        self.frame_lb = customtkinter.CTkLabel(self,
                                               text="Classification options",
                                               font=FONT_HELV_MEDIUM_B,
                                               anchor='center',
                                               justify='center')
        self.classification_btn = customtkinter.CTkButton(self,
                                                          text="Run classification",
                                                          command=self.classification_event)
        self.model_lb = customtkinter.CTkLabel(self,
                                               text="Select model",
                                               font=FONT_HELV_SMALL_B)
        self.model_cbox = customtkinter.CTkComboBox(self,
                                                    values=list(self.MODELS.keys()))
        self.stride_ckb = customtkinter.CTkCheckBox(self, text="Use stride", variable=self.use_stride)

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
        self.model_cbox.grid(row=2, column=0, padx=15, sticky="ew")
        self.classification_btn.grid(row=9, column=5)
        self.stride_ckb.grid(row=9, column=4)

    def classification_event(self) -> bool:

        if not self.__las_handler.file_loaded:
            CTkMessagebox(title="File not loaded", message="Whoops!\n"
                                                           "Load .las file first.", icon="cancel")
            return False

        try:
            CTkMessagebox(title="Classificaiton in progress...",
                          message="Working on it!\n"
                          "Please be patient! Classificaiton can take a while depending on"
                          " the number of points and the speed of your computer.\n\n",
                          icon="info")

            self.classification_btn.configure(state=customtkinter.DISABLED)
            threading.Thread(target=self.run_classification).start()
        except Exception as e:
            self.classification_btn.configure(state=customtkinter.NORMAL)
            pass
        return True

    def run_classification(self):
        model = ClassificationUtils.load_joblib(self.MODELS[self.selected_model])

        if self.use_stride.get():
            self.classification_stride = self.get_classification_stride()
            print("Classification stride is ", self.classification_stride)
            X, _ = ClassificationUtils.prepare_data_prediction(self.las_handler.data_frame[::self.classification_stride])
            prediction = model.predict(X)
            prediction_fixed = ClassificationFrame.fix_prediction(prediction, self.classification_stride)
            if len(prediction_fixed) != len(self.las_handler.data_frame['classification']):
                prediction_fixed = prediction_fixed[:len(self.las_handler.data_frame['classification'])]
            self.las_handler.data_frame['classification'] = prediction_fixed

        else:
            X, _ = ClassificationUtils.prepare_data_prediction(self.las_handler.data_frame)
            prediction = model.predict(X)
            self.las_handler.data_frame['classification'] = prediction

        self.classification_btn.configure(state=customtkinter.NORMAL)
        CTkMessagebox(title="Classification completed", message=f"All done!\n\n Classification completed.",
                      icon="check", option_1="OK")
        self.__master.invoke_update_file_description()
        print(self.las_handler.data_frame["classification"])

    def get_classification_stride(self) -> int:
        return self.__master.get_stride()

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
