import os
import subprocess
import threading
import json

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from las_handler import *
from resources.fonts import *


class VisualisationFrame(ctk.CTkFrame):
    __file_path: str
    __las_handler: LasHandler
    __rendering_stride: int
    __rendering_method: str
    __generated_points_count: int
    __too_many_points: bool

    # Widgets definitions
    frame_lb: ctk.CTkLabel
    method_lb: ctk.CTkLabel
    stride_lb: ctk.CTkLabel
    rendering_progress_lb: ctk.CTkLabel
    generated_points_count_lb: ctk.CTkLabel
    batches_count_lb: ctk.CTkLabel
    batching_lb: ctk.CTkLabel
    rendered_batch_lb: ctk.CTkLabel
    render_btn: ctk.CTkButton
    method_cbox: ctk.CTkComboBox
    rendered_batch_cbox: ctk.CTkComboBox
    stride_sld: ctk.CTkSlider
    stride_ebox: ctk.CTkEntry
    batches_count_sld: ctk.CTkSlider
    batch_ckb: ctk.CTkCheckBox

    def __init__(self, master, las_handler: LasHandler, **kwargs):
        super().__init__(master, **kwargs)

        self.__master = master
        self.las_handler = las_handler

        self.rendering_stride = 15
        self.generated_points_count = 0
        self.number_of_batches = 2
        self.selected_batch = 1

        self.rendering_methods_limits = {"pptk": 10000000,
                                         "plotly": 600000,
                                         "polyscope": 1000000}

        self.rendering_method = list(self.rendering_methods_limits.keys())[0]

        self.set_frame_grid(10, 10)

        self.batching_enabled_variable = ctk.BooleanVar(value=False)
        self.selected_batch_variable = ctk.StringVar(value=str(self.selected_batch))

        self.initialize_widgets()
        self.set_widgets_default_configuration()
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
                                     text="Visualisation options",
                                     font=FONT_HELV_MEDIUM_B,
                                     anchor='center',
                                     justify='center')
        self.render_btn = ctk.CTkButton(self,
                                        text="Render visualisation",
                                        command=self.render_event)
        self.method_lb = ctk.CTkLabel(self,
                                      text="Rendering tool",
                                      font=FONT_HELV_SMALL_B)
        self.method_cbox = ctk.CTkComboBox(self,
                                           values=list(self.rendering_methods_limits.keys()),
                                           command=self.update_rendering_method_event)
        self.stride_lb = ctk.CTkLabel(self,
                                      text="Rendering stride")
        self.stride_sld = ctk.CTkSlider(self,
                                        from_=1,
                                        to=100,
                                        number_of_steps=100,
                                        progress_color='#3a7ebf',
                                        command=self.update_rendering_stride_event)
        self.stride_ebox = ctk.CTkEntry(self,
                                        width=50,
                                        height=28,
                                        textvariable=ctk.StringVar(
                                            value=str(self.rendering_stride)))
        self.rendering_progress_lb = ctk.CTkLabel(self,
                                                  text=" ")
        self.batch_ckb = ctk.CTkCheckBox(self,
                                         text="Enable",
                                         variable=self.batching_enabled_variable,
                                         command=self.batching_changed_state_event)
        self.generated_points_count_lb = ctk.CTkLabel(self, text="")
        self.batching_lb = ctk.CTkLabel(self,
                                        text="Batching",
                                        font=FONT_HELV_SMALL_B)
        self.batches_count_lb = ctk.CTkLabel(self,
                                             text="Number of batches")
        self.batches_count_sld = ctk.CTkSlider(self,
                                               from_=1,
                                               to=10,
                                               number_of_steps=10,
                                               progress_color='#3a7ebf',
                                               command=self.update_batches_count_event)
        self.rendered_batch_lb = ctk.CTkLabel(self,
                                              text="Rendered batch #:")
        self.rendered_batch_cbox = ctk.CTkComboBox(self,
                                                   width=100,
                                                   values=[str(i) for i in
                                                           range(1, self.number_of_batches + 1)],
                                                   variable=self.selected_batch_variable)

    def set_widgets_positioning(self) -> None:
        """
        Sets the grid positioning for all the widgets in the GUI.

        This function arranges widgets within the GUI using the tkinter grid geometry manager.
        It defines the row, column, columnspan, and sticky options for each widget to achieve the desired layout.

        Returns:
            None
        """
        self.frame_lb.grid(row=0, column=0, columnspan=10, sticky="nsew")
        self.method_lb.grid(row=1, column=0, padx=15, sticky="w")
        self.method_cbox.grid(row=2, column=0, padx=15, sticky="ew")
        self.stride_lb.grid(row=3, column=0, columnspan=2, padx=15, sticky="w")
        self.stride_sld.grid(row=4, column=0, columnspan=2, padx=15, sticky="ew")
        self.generated_points_count_lb.grid(row=5, column=0, columnspan=2, padx=20, sticky="w")
        self.stride_ebox.grid(row=4, column=2, padx=15, sticky="w")
        self.render_btn.grid(row=9, column=9, padx=10, pady=10, sticky="e")
        self.rendering_progress_lb.grid(row=9, column=7, columnspan=2, sticky="w")
        self.batching_lb.grid(row=1, column=3, sticky="w")
        self.batch_ckb.grid(row=2, column=3, sticky="w")
        self.batches_count_lb.grid(row=3, column=3, sticky="w")
        self.batches_count_sld.grid(row=4, column=3, sticky="w")
        self.rendered_batch_lb.grid(row=3, column=4, sticky="w")
        self.rendered_batch_cbox.grid(row=4, column=4, sticky="w")

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
        self.batches_count_sld.set(self.number_of_batches)
        self.batches_count_sld.configure(state="disabled")
        self.rendered_batch_cbox.configure(state="disabled")

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

    def stride_entry_event(self, entry: ctk.CTkEntry) -> None:
        """
        Event handler for stride entry.

        Args:
            entry (ctk.CTkEntry): The entry widget.

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
                entry.configure(textvariable=ctk.StringVar(value=str(100)))

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
            CTkMessagebox(title="File not loaded", message="Whoops!\n\n"
                                                           "Load .las file first.", icon="cancel")
            return False

        if self.too_many_points:
            msg = CTkMessagebox(title="Too many points", message="Woah!\n\n"
                                                                 "That's a lot of points!\n"
                                                                 f"Selected rendering method ({self.rendering_method}) "
                                                                 f"can only render around "
                                                                 f"{self.rendering_methods_limits[self.rendering_method]}"
                                                                 f" points smoothly.\n"
                                                                 f"Consider using another method or display just a "
                                                                 f"part of the file using batching.\n\n"
                                                                 "Do you want to continue?",
                                icon="warning", options=["Yes", "No"])
            if msg.get() == "No":
                return False

        try:
            self.render_btn.configure(state=ctk.DISABLED)
            if self.rendering_method == list(self.rendering_methods_limits.keys())[2]:
                CTkMessagebox(title="Rendering...", message="Working on it!\n\n"
                                                            "Please be patient! Rendering can take a while depending on"
                                                            " the number of points and the speed of your computer.\n\n"
                                                            "The result should pop up in a separate window!",
                              icon="info")
                #threading.Thread(target=self.render_polyscope).start()
                self.render_polyscope()
            if self.rendering_method == list(self.rendering_methods_limits.keys())[1]:
                CTkMessagebox(title="Rendering...", message="Working on it!\n\n"
                                                            "Please be patient! Rendering can take a while depending on"
                                                            " the number of points and the speed of your computer.\n\n"
                                                            "The result should pop up in your main browser!",
                              icon="info")
                threading.Thread(target=self.render_plotly).start()
            elif self.rendering_method == list(self.rendering_methods_limits.keys())[0]:
                CTkMessagebox(title="Rendering...", message="Working on it!\n\n"
                                                            "Please be patient! Rendering can take a while depending on"
                                                            " the number of points and the speed of your computer.\n\n"
                                                            "The result should pop up in a separate window!",
                              icon="info")
                threading.Thread(target=self.render_pptk).start()
        except Exception as e:
            CTkMessagebox(title="Error", message="That's not good!\n\n"
                                                 "Visualisation failed!\n\n"
                                                 f"{str(e)}", icon="cancel")
            self.render_btn.configure(state=ctk.NORMAL)
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

    def update_batches_count_event(self, slider_value: float) -> None:
        if self.batching_enabled_variable:
            self.number_of_batches = round(slider_value)
        self.rendered_batch_cbox.configure(values=[str(i) for i in range(1, self.number_of_batches + 1)])

    def update_generated_points_count_lb(self):
        """
        Update the label showing the count of generated points.

        Args:
            color (str): Optional color for the label.

        Returns:
            None
        """
        if self.__las_handler.file_loaded:
            self.generated_points_count = round(self.las_handler.las.header.point_count / self.rendering_stride)
            formatted_generated_points_count = f"{self.generated_points_count:,}".replace(',', ' ')
            self.generated_points_count_lb.configure(text=f"{formatted_generated_points_count} points will"
                                                          f" be rendered.")
        if not self.check_rendering_method_limit(self.generated_points_count):
            self.generated_points_count_lb.configure(text_color="orange")
            self.too_many_points = True
        else:
            self.generated_points_count_lb.configure(text_color="white")
            self.too_many_points = False

    def check_rendering_method_limit(self, point_count: int) -> bool:
        if point_count > self.rendering_methods_limits[self.rendering_method]:
            return False
        return True

    @staticmethod
    def select_dataframe_batch(p: int, q: int, dataframe: pd.DataFrame) -> pd.DataFrame:
        batch_size = len(dataframe) // q

        start_index = (p - 1) * batch_size
        end_index = p * batch_size if p < q else None

        return dataframe.iloc[start_index:end_index]

    def update_rendering_method_event(self, rendering_method: str) -> None:
        """
        Update the rendering method used for visualizing the data.

        Args:
            rendering_method (str): The new rendering method to be used.

        Returns:
            None
        """
        self.rendering_method = rendering_method

    def batching_changed_state_event(self) -> None:
        if self.batching_enabled_variable.get():
            self.batches_count_sld.configure(state="normal")
            self.rendered_batch_cbox.configure(state="normal")
        else:
            self.batches_count_sld.configure(state="disabled")
            self.rendered_batch_cbox.configure(state="disabled")

    def render_plotly(self) -> None:
        """
        Renders LAS data using Plotly.

        Returns:
            None
        """
        self.rendering_progress_lb.configure(text="Please wait. Rendering in progress...", text_color="red")
        if self.batching_enabled_variable.get():
            df_batch = VisualisationFrame.select_dataframe_batch(int(self.selected_batch_variable.get()),
                                                                 self.number_of_batches, self.las_handler.data_frame)
            self.las_handler.visualize_las_plotly(self.rendering_stride, df_batch)
        else:
            self.las_handler.visualize_las_plotly(self.rendering_stride)

        self.rendering_progress_lb.configure(text="Done!", text_color="green")
        self.render_btn.configure(state="normal")

    def render_polyscope(self) -> None:
        """
        Renders LAS data using Polyscope.

        Returns:
            None
        """

        self.rendering_progress_lb.configure(text="Please wait. Rendering in progress...", text_color="red")
        try:
            if self.batching_enabled_variable.get():
                df_batch = VisualisationFrame.select_dataframe_batch(int(self.selected_batch_variable.get()),
                                                                     self.number_of_batches, self.las_handler.data_frame)
                self.las_handler.visualize_las_polyscope(self.rendering_stride, df_batch)
            else:
                self.las_handler.visualize_las_polyscope(self.rendering_stride)
        except RuntimeError as e:
            CTkMessagebox(title="Error", message="That's not good!\n\n"
                                                 "Unexpected polyscope error ocurred!\nPlease try again.\n\n"
                                                 f"{str(e)}", icon="cancel")
        except Exception as e:
            CTkMessagebox(title="Error", message="That's not good!\n\n"
                                                 "Visualisation failed!\n\n"
                                                 f"{str(e)}", icon="cancel")

        self.rendering_progress_lb.configure(text="Done!", text_color="green")
        self.render_btn.configure(state="normal")

    def render_pptk(self) -> None:
        """
        Renders LAS data using pptk.

        Returns:
            None
        """
        self.rendering_progress_lb.configure(text="Please wait. Rendering in progress...", text_color="red")

        python37_path = r"/usr/local/bin/python3.7"
        print(python37_path)
        script_path = r".\neptunseye\script_pptk.py"
        dataframe_temp_file_path = ".tempdf.csv"

        self.save_selected_columns_to_csv(['X', 'Y', 'Z', 'red', 'green', 'blue', 'classification'])

        os.environ.copy()
        subprocess.run([python37_path, script_path, dataframe_temp_file_path], check=True, text=True)
        self.rendering_progress_lb.configure(text="Done!", text_color="green")
        self.render_btn.configure(state="normal")

    def save_selected_columns_to_csv(self, selected_columns, filename=".tempdf.csv") -> None:
        """
        Save selected columns of LAS data to a CSV file.

        Args:
            selected_columns (list): List of column names to be saved.
            filename (str): Name of the CSV file. Default is ".tempdf.csv".

        Returns:
            None
        """

        if self.batching_enabled_variable.get():
            data_frame = VisualisationFrame.select_dataframe_batch(int(self.selected_batch_variable.get()),
                                                                   self.number_of_batches, self.las_handler.data_frame)
            df_stride = data_frame.iloc[::self.rendering_stride].copy()
            selected_df = df_stride[selected_columns]
            selected_df.to_csv(filename, index=False)
        else:
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

    @property
    def too_many_points(self) -> bool:
        return self.__too_many_points

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

    @too_many_points.setter
    def too_many_points(self, value: bool) -> None:
        self.__too_many_points = bool(value)
