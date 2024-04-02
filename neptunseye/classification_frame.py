import customtkinter

from las_handler import *
from resources.fonts import *
from classification_utils import ClassificationUtils


class ClassificationFrame(customtkinter.CTkFrame):
    __file_path: str
    __las_handler: LasHandler

    frame_lb: customtkinter.CTkLabel
    model_lb: customtkinter.CTkLabel
    model_cbox: customtkinter.CTkComboBox
    classification_btn: customtkinter.CTkButton

    def __init__(self, master, las_handler: LasHandler, **kwargs):
        super().__init__(master, **kwargs)

        self.MODELS = {"ExtraTreesClassifier": "resources\\models\\aha41.joblib"}

        self.selected_model = "ExtraTreesClassifier"

        self.__las_handler = las_handler

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

    def classification_event(self) -> None:
        model = ClassificationUtils.load_joblib(self.MODELS[self.selected_model])

        X, _ = ClassificationUtils.prepare_data_prediction(self.las_handler.data_frame)
        prediction = model.predict(X)

        self.las_handler.data_frame["classification"] = prediction
        print("Success!")

    @property
    def las_handler(self) -> LasHandler:
        return self.__las_handler

    @las_handler.setter
    def las_handler(self, value: LasHandler) -> None:
        self.__las_handler = value

