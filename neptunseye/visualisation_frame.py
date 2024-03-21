import threading

import customtkinter
from CTkMessagebox import CTkMessagebox

from las_handler import *
from resources.fonts import *


class VisualisationFrame(customtkinter.CTkTabview):
    __file_path: str
    __las_handler: LasHandler
    __rendering_stride: int
    __rendering_method: str

    def __init__(self, master, las_handler: LasHandler, **kwargs):
        super().__init__(master, **kwargs)

        self.__master = master
        self.__las_handler = las_handler

        self.rendering_stride = 15
        self.rendering_method = "plotly"

        self.add("Plotting")
        self.add("3D Rendering")

        self.tab_2d = self.tab("Plotting")
        self.tab_3d = self.tab("3D Rendering")

        self.tab_2d.grid_columnconfigure((1, 2, 3), weight=1)
        self.tab_2d.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)

        # "Plotting" tab
        self.frame_label = customtkinter.CTkLabel(self.tab_2d, text="Visualisation options", font=FONT_HELV_MEDIUM_B,
                                                  anchor='center', justify='center')
        self.button = customtkinter.CTkButton(self.tab_2d, text="Render plot", command=self.render_2d_event)
        self.method_label = customtkinter.CTkLabel(self.tab_2d, text="Plotting tool")
        self.method_combo = customtkinter.CTkComboBox(self.tab_2d, values=["plotly", "matplotlib"],
                                                      command=self.update_rendering_method_event)
        self.stride_label = customtkinter.CTkLabel(self.tab_2d, text="Rendering stride")
        self.stride_slider = customtkinter.CTkSlider(self.tab_2d, from_=1, to=100, number_of_steps=100,
                                                     progress_color='#3a7ebf', command=self.update_stride_event)
        self.stride_tbox = customtkinter.CTkTextbox(self.tab_2d, width=50, height=10)
        self.plotting_in_progress = customtkinter.CTkLabel(self.tab_2d, text=" ")
        self.batch_variable = customtkinter.BooleanVar(value=False)
        self.batch_ckb = customtkinter.CTkCheckBox(self.tab_2d, text="Batching", variable=self.batch_variable)

        # Default values
        self.method_combo.configure(state="readonly")
        self.stride_slider.set(self.rendering_stride)
        self.stride_tbox.insert("0.0", self.rendering_stride, "end")
        self.batch_ckb.configure(state="disabled")

        # Positioning
        self.frame_label.grid(row=0, column=0, columnspan=4, sticky="ew")
        self.method_label.grid(row=1, column=0, padx=10, sticky="ew")
        self.method_combo.grid(row=2, column=0, padx=10, sticky="ew")
        self.batch_ckb.grid(row=2, column=1)
        self.stride_label.grid(row=3, column=0, padx=10, sticky="ew")
        self.stride_slider.grid(row=4, column=0, columnspan=2, padx=10, sticky="ew")
        self.stride_tbox.grid(row=4, column=2, padx=10, sticky="w")
        self.button.grid(row=9, column=3)
        self.plotting_in_progress.grid(row=9, column=1)

    def render_2d_event(self) -> bool:

        if self.__las_handler.file_loaded is False:
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
        except Exception as e:
            CTkMessagebox(title="Error", message=str(e), icon="cancel")
            return False

        return True

    def update_stride_event(self, slider_value: float) -> None:
        self.rendering_stride = round(slider_value)
        self.stride_tbox.delete("0.0", "end")
        self.stride_tbox.insert("0.0", self.rendering_stride, "end")

    def update_rendering_method_event(self, rendering_method: str) -> None:
        self.rendering_method = rendering_method
        if rendering_method == "matplotlib":
            self.batch_ckb.configure(state="normal")
        else:
            self.batch_ckb.deselect()
            self.batch_ckb.configure(state="disabled")

    def render_plotly_async(self):
        self.plotting_in_progress.configure(text="Plotting in progress...", text_color="red")
        self.__las_handler.visualize_las_2d_plotly(self.rendering_stride)
        self.plotting_in_progress.configure(text="Done!", text_color="green")

    def render_matplotlib_async(self):
        self.plotting_in_progress.configure(text="Plotting in progress...", text_color="red")
        self.__las_handler.visualize_las_2d_matplotlib(self.rendering_stride, self.batch_variable.get(),
                                                       batch_size=5000,
                                                       pause_interval=0.05)
        self.plotting_in_progress.configure(text="Done!", text_color="green")

    @property
    def rendering_stride(self) -> int:
        return self.__rendering_stride

    @property
    def rendering_method(self) -> str:
        return self.__rendering_method

    @rendering_stride.setter
    def rendering_stride(self, value: int) -> None:
        self.__rendering_stride = value

    @rendering_method.setter
    def rendering_method(self, value: str) -> None:
        self.__rendering_method = value
