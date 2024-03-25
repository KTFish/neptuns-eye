import os
import subprocess
import threading

import customtkinter
from CTkMessagebox import CTkMessagebox

from las_handler import *
from resources.fonts import *


class VisualisationFrame(customtkinter.CTkFrame):
    __file_path: str
    __las_handler: LasHandler
    __rendering_stride: int
    __rendering_method: str
    __generated_points_count: int

    # Widgets definitions
    # TODO: Comment every widgets' placement and function
    frame_lb: customtkinter.CTkLabel
    method_lb: customtkinter.CTkLabel
    stride_lb: customtkinter.CTkLabel
    plotting_progress_lb: customtkinter.CTkLabel
    generated_points_count_lb: customtkinter.CTkLabel
    render_btn: customtkinter.CTkButton
    method_cbox: customtkinter.CTkComboBox
    stride_sld: customtkinter.CTkSlider
    stride_ebox: customtkinter.CTkEntry
    batch_ckb: customtkinter.CTkCheckBox

    def __init__(self, master, las_handler: LasHandler, **kwargs):
        super().__init__(master, **kwargs)

        self.__master = master
        self.las_handler = las_handler

        self.rendering_stride = 15
        self.generated_points_count = 0
        self.rendering_method = "plotly"

        self.set_frame_grid(10, 10)

        self.batch_variable = customtkinter.BooleanVar(value=False)

        self.initialize_widgets()

        self.set_widgets_default_configuration()

        self.set_widgets_positioning()

    def initialize_widgets(self):
        """Initializes all the widgets used in the GUI.

        This function creates instances of various CustomTkinter widgets
        and configures their basic properties. These widgets represent the
        user interface elements for interacting with the application.

        Returns:
            None
        """
        self.frame_lb = customtkinter.CTkLabel(self, text="Visualisation options",
                                               font=FONT_HELV_MEDIUM_B,
                                               anchor='center',
                                               justify='center')
        self.render_btn = customtkinter.CTkButton(self, text="Render visualisation",
                                                  command=self.render_event)
        self.method_lb = customtkinter.CTkLabel(self, text="Rendering tool")
        self.method_cbox = customtkinter.CTkComboBox(self, values=["plotly", "matplotlib", "pptk"],
                                                     command=self.update_rendering_method_event)
        self.stride_lb = customtkinter.CTkLabel(self, text="Rendering stride")
        self.stride_sld = customtkinter.CTkSlider(self, from_=1,
                                                  to=100,
                                                  number_of_steps=100,
                                                  progress_color='#3a7ebf',
                                                  command=self.update_rendering_stride_event)
        self.stride_ebox = customtkinter.CTkEntry(self, width=50,
                                                  height=10,
                                                  textvariable=customtkinter.StringVar(
                                                      value=str(self.rendering_stride)))
        self.plotting_progress_lb = customtkinter.CTkLabel(self, text=" ")

        self.batch_ckb = customtkinter.CTkCheckBox(self, text="Batching",
                                                   variable=self.batch_variable)
        self.generated_points_count_lb = customtkinter.CTkLabel(self, text="")

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

    def set_widgets_positioning(self) -> None:
        """
        Sets the grid positioning for all the widgets in the GUI.

        This function arranges widgets within the GUI using the tkinter grid geometry manager.
        It defines the row, column, columnspan, and sticky options for each widget to achieve the desired layout.

        Returns:
            None
        """
        self.frame_lb.grid(row=0, column=0, columnspan=9, sticky="ew")
        self.method_lb.grid(row=1, column=0, padx=10, sticky="ew")
        self.method_cbox.grid(row=2, column=0, padx=10, sticky="ew")
        self.batch_ckb.grid(row=2, column=1)
        self.stride_lb.grid(row=3, column=0, columnspan=2, padx=10, sticky="ew")
        self.stride_sld.grid(row=4, column=0, columnspan=2, padx=10, sticky="ew")
        self.generated_points_count_lb.grid(row=5, column=0, columnspan=2, padx=10, sticky="w")
        self.stride_ebox.grid(row=4, column=2, padx=10, sticky="w")
        self.render_btn.grid(row=9, column=3)
        self.plotting_progress_lb.grid(row=9, column=1)

    def set_widgets_default_configuration(self) -> None:
        """
        Sets the default configuration for the GUI widgets.

       This function configures various aspects of the widgets used in the GUI to establish their initial state and
       behavior.

       Returns:
           None
        """
        self.stride_ebox.configure(validate="all",
                                   validatecommand=(self.stride_ebox.register(self.stride_entry_validate), "%S"))
        self.stride_ebox.bind("<KeyRelease>", lambda event: self.stride_entry_event(self.stride_ebox))
        self.method_cbox.configure(state="readonly")
        self.stride_sld.set(self.rendering_stride)
        self.batch_ckb.configure(state="disabled")

    @staticmethod
    def stride_entry_validate(text: str) -> bool:
        """Validates the entered text in the stride entry widget.

        This function  ensures that the entered text meets the following criteria:

        - The text is either empty or consists only of digits (0-9).

        Args:
            text: The text entered in the stride entry widget.

        Returns:
            bool: True if the text is valid (empty or digits only), False otherwise.
        """
        if text.isdigit() or text == "":
            return True
        return False

    def stride_entry_event(self, entry: customtkinter.CTkEntry) -> None:
        """
        Event handler for stride entry.

        Args:
            entry (customtkinter.CTkEntry): The entry widget.

        Returns:
            None
        """
        entry_value = entry.get()
        if entry_value != '':
            rendering_stride = int(entry_value)
            if 1 <= rendering_stride <= 100:
                self.rendering_stride = rendering_stride
                self.stride_sld_update(rendering_stride)
            if rendering_stride > 100:
                self.rendering_stride = 100
                self.stride_sld_update(100)
                entry.configure(textvariable=customtkinter.StringVar(value=str(100)))

            self.update_generated_points_count_lb()

    def stride_sld_update(self, value: int) -> None:
        """
        Update the value of the stride slider.

        Args:
            value (int): The new value for the stride slider.

        Returns:
            None
        """
        self.stride_sld.set(value)

    def render_event(self) -> bool:
        """
        Initiates the rendering process based on the selected method.

        Returns:
            bool: True if rendering is successfully initiated, False otherwise.
        """
        if not self.__las_handler.file_loaded:
            CTkMessagebox(title="File not loaded", message="Whoops!\n"
                                                           "Load .las file first.", icon="cancel")
            return False

        try:
            if self.rendering_method == 'plotly':
                CTkMessagebox(title="Rendering...", message="Working on it!\n"
                                                            "Please be patient! Rendering can take a while depending on"
                                                            " the number of points and the speed of your computer.\n\n"
                                                            "The result should pop up in your main browser!",
                              icon="info")
                threading.Thread(target=self.render_plotly_async).start()
            elif self.rendering_method == 'matplotlib':
                CTkMessagebox(title="Rendering...", message="Working on it!\n"
                                                            "Please be patient! Rendering can take a while depending on"
                                                            " the number of points and the speed of your computer.\n"
                                                            "Take note that matplotlib is slow with large data sets.\n\n"
                                                            "The result should pop up in a separate window!",
                              icon="info")
                threading.Thread(target=self.render_matplotlib_async).start()
            elif self.rendering_method == 'pptk':
                CTkMessagebox(title="Rendering...", message="Working on it!\n"
                                                            "Please be patient! Rendering can take a while depending on"
                                                            " the number of points and the speed of your computer.\n\n"
                                                            "The result should pop up in a separate window!",
                              icon="info")
                self.render_pptk()
        except Exception as e:
            CTkMessagebox(title="Error", message=str(e), icon="cancel")
            return False

        return True

    def update_rendering_stride_event(self, slider_value: float) -> None:
        """
        Event handler for updating the rendering stride.

        Args:
            slider_value (float): The value of the slider.

        Returns:
            None
        """
        self.update_generated_points_count_lb()
        self.rendering_stride = round(slider_value)
        self.stride_ebox.delete(0, "end")
        self.stride_ebox.insert(0, self.rendering_stride)

    def update_generated_points_count_lb(self, color=None):
        """
        Update the label showing the count of generated points.

        Args:
            color (str): Optional color for the label.

        Returns:
            None
        """
        if self.__las_handler.file_loaded:
            self.generated_points_count = round(self.__las_handler.las.header.point_count / self.rendering_stride)
            formatted_generated_points_count = f"{self.generated_points_count:,}".replace(',', ' ')
            self.generated_points_count_lb.configure(text=f"{formatted_generated_points_count} points will"
                                                          f" be generated.")
        if color is not None:
            self.generated_points_count_lb.configure(text_color=color)

    def update_rendering_method_event(self, rendering_method: str) -> None:
        # TODO: TO BE REMOVED
        self.rendering_method = rendering_method
        if rendering_method == "matplotlib":
            self.batch_ckb.configure(state="normal")
        else:
            self.batch_ckb.deselect()
            self.batch_ckb.configure(state="disabled")

    def render_plotly_async(self):
        """
        Asynchronously renders LAS data using Plotly.

        Returns:
            None
        """
        self.plotting_progress_lb.configure(text="Plotting in progress...", text_color="red")
        self.__las_handler.visualize_las_2d_plotly(self.rendering_stride)
        self.plotting_progress_lb.configure(text="Done!", text_color="green")

    def render_matplotlib_async(self):
        """
        Asynchronously renders LAS data using Matplotlib.

        Returns:
            None
        """
        self.plotting_progress_lb.configure(text="Plotting in progress...", text_color="red")
        self.__las_handler.visualize_las_2d_matplotlib(self.rendering_stride,
                                                       batch_size=5000,
                                                       pause_interval=0.05)
        self.plotting_progress_lb.configure(text="Done!", text_color="green")

    def render_pptk(self):
        local_app_data_path = os.environ.get("LOCALAPPDATA", "")
        python37_path = local_app_data_path + "\\Programs\\Python\\python37\\python.exe"
        print(python37_path)
        script_path = "script_pptk.py"
        dataframe_temp_file_path = ".tempdf.csv"

        self.save_selected_columns_to_csv(['X', 'Y', 'Z', 'red', 'green', 'blue'])

        os.environ.copy()
        subprocess.run([python37_path, script_path, dataframe_temp_file_path], check=True, text=True)

    def save_selected_columns_to_csv(self, selected_columns, filename=".tempdf.csv") -> None:
        """
        Save selected columns of LAS data to a CSV file.

        Args:
            selected_columns (list): List of column names to be saved.
            filename (str): Name of the CSV file. Default is ".tempdf.csv".

        Returns:
            None
        """

        df_stride = self.las_handler.data_frame.iloc[::self.rendering_stride].copy()
        selected_df = df_stride[selected_columns]
        selected_df.to_csv(filename, index=False)

    @property
    def rendering_stride(self) -> int:
        return self.__rendering_stride

    @property
    def rendering_method(self) -> str:
        return self.__rendering_method

    @property
    def generated_points_count(self) -> int:
        return self.__generated_points_count

    @property
    def las_handler(self) -> LasHandler:
        return self.__las_handler

    @rendering_stride.setter
    def rendering_stride(self, value: int) -> None:
        self.__rendering_stride = value

    @rendering_method.setter
    def rendering_method(self, value: str) -> None:
        self.__rendering_method = value

    @generated_points_count.setter
    def generated_points_count(self, value: int) -> None:
        self.__generated_points_count = value

    @las_handler.setter
    def las_handler(self, value: LasHandler) -> None:
        self.__las_handler = value
