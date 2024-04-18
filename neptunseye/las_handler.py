from typing import List

import laspy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go


class LasHandler(object):

    __file_path: str
    __file_loaded: bool
    __las: laspy.LasData
    visualisation_figure: plt.Figure
    __exception: Exception
    __data_frame: pd.DataFrame
    __unique_classes: List[int]

    def __init__(self, file_path: str = None) -> None:

        self.visualisation_figure = None
        self.file_loaded = False
        self.__exception = None
        self.data_frame = None
        self.unique_classes = []

        if file_path is not None:
            self.__file_path = file_path
            try:
                self.las = laspy.read(self.__file_path)
                self.file_loaded = True
            except FileNotFoundError:
                self.__exception = FileNotFoundError("File not found" + file_path)
            except Exception as e:
                self.__exception = e

    def visualize_las_2d_plotly(self, stride: int = 25, data_frame: pd.DataFrame = None):

        if data_frame is None:
            data_frame = self.data_frame
        else:
            data_frame = data_frame

        predefined_colors = {
            11: '#FF0000',  # Red
            13: '#0000FF',  # Blue
            25: '#FFFF00',  # Yellow
            0: '#800080',  # Purple
            1: '#008000',  # Green
            15: '#FFA500',  # Orange
            17: '#00FFFF',  # Cyan
            19: '#FFC0CB'  # Pink
        }

        points = data_frame[['X', 'Y', 'Z']].values
        colors = data_frame[['red', 'green', 'blue']].values / 65535.0

        points = points[::stride]
        colors = colors[::stride]

        unique_classes_count = len(self.unique_classes)
        if unique_classes_count <= 1 and (self.unique_classes[0] == 0 or self.unique_classes[0] == 1):
            point_colors = ['#%02x%02x%02x' % tuple(int(255 * c) for c in color) for color in colors]
        else:
            classification = data_frame['classification']
            classification = classification[::stride]
            point_colors = [predefined_colors.get(c, '#FFFFFF') for c in classification]

        fig = go.Figure()

        fig.add_trace(go.Scatter3d(
            x=points[:, 0],
            y=points[:, 1],
            z=points[:, 2],
            mode='markers',
            marker=dict(
                size=2,
                color=point_colors
            )
        ))

        fig.update_layout(scene=dict(
            xaxis=dict(showticklabels=False),
            yaxis=dict(showticklabels=False),
            zaxis=dict(showticklabels=False)
        ))

        fig.show()

    def __get_unique_classes(self) -> List[int]:
        return self.data_frame['classification'].unique().tolist()

    def create_dataframe(self):

        columns = [dimension.name for dimension in self.las.point_format.dimensions]
        data = np.vstack([getattr(self.las, dimension) for dimension in columns]).transpose()
        df = pd.DataFrame(data, columns=columns)
        return df

    @property
    def las(self) -> laspy.LasData:
        return self.__las

    @property
    def file_loaded(self) -> bool:
        return self.__file_loaded

    @property
    def exception(self) -> Exception:
        return self.__exception

    @property
    def unique_classes(self) -> List[int]:
        return self.__get_unique_classes()

    @las.setter
    def las(self, las: laspy.LasData) -> None:
        self.__las = las

    @file_loaded.setter
    def file_loaded(self, file_loaded: bool) -> None:
        self.__file_loaded = file_loaded

    @unique_classes.setter
    def unique_classes(self, unique_classes: List[int]) -> None:
        self.__unique_classes = unique_classes

