import laspy
import numpy as np
import matplotlib.pyplot as plt
from laspy import LasData
from matplotlib.figure import Figure


class LasHandler(object):

    __file_path: str
    __file_loaded: bool
    __las: LasData
    visualisation_figure: Figure

    def __init__(self, file_path: str = None) -> None:

        self.visualisation_figure = None
        self.file_loaded = False

        if file_path is not None:
            self.__file_path = file_path
            try:
                self.las = laspy.read(self.__file_path)
                self.file_loaded = True
            except FileNotFoundError:
                print("Las file not found!", self.__file_path)

    def visualize_las_2d(self):

        # Extract x, y, z coordinates
        x = self.las.x
        y = self.las.y
        z = self.las.z

        # Extract RGB values from the LAS file
        r = self.las.red / 65535.0  # Normalize the RGB values to [0, 1]
        g = self.las.green / 65535.0
        b = self.las.blue / 65535.0

        colors = np.column_stack((r, g, b))

        # Create a 3D scatter plot with specified colors
        fig = plt.figure()
        fig.subplots_adjust(left=0, right=1, bottom=0, top=1)  # Remove margins
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(x, y, z, marker='.', c=colors, s=0.5)  # Use extracted RGB values as color

        # Set labels and title
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.margins(0)
        ax.set_title('')

        # Show plot
        # plt.show()
        self.visualisation_figure = fig

    @property
    def las(self) -> LasData:
        return self.__las

    @property
    def file_loaded(self) -> bool:
        return self.__file_loaded

    @las.setter
    def las(self, las: LasData) -> None:
        self.__las = las

    @file_loaded.setter
    def file_loaded(self, file_loaded: bool) -> None:
        self.__file_loaded = file_loaded
