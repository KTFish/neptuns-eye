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

        class_color_map = {
            0: '#FFFFFF',  # 0 never classified - white
            1: '#000000',  # 1 unclassified - black
            11: '#0000FF',  # 11 ground - blue
            13: '#007F00',  # 13 vegetation - green
            15: '#00FFFF',  # 15 building - cyan
            17: '#7F7F7F',  # 17 main road - gray
            19: '#FF0000',  # 19 power lines - red
            25: '#994B00',  # 25 minor road - brown
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
            point_colors = [class_color_map.get(c, '#FFFFFF') for c in classification]

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

    def visualize_las_2d_matplotlib(self, stride: int = 15, data_frame: pd.DataFrame = None, **kwargs):
        """kwargs: batch_size, pause_interval"""

        if data_frame is None:
            data_frame = self.data_frame
        else:
            data_frame = data_frame

        points = data_frame[['X', 'Y', 'Z']].values
        colors = data_frame[['red', 'green', 'blue']].values / 65535.0

        points = points[::stride]
        colors = colors[::stride]

        fig = plt.figure(figsize=(14, 12))
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
        ax.set_xlabel('')
        ax.set_ylabel('')
        ax.set_zlabel('')

        total_points = len(points)
        counter_text_obj = ax.text2D(0.05, 0.95, '', transform=ax.transAxes)

        for start_idx in range(0, total_points, kwargs['batch_size']):
            end_idx = min(start_idx + kwargs['batch_size'], total_points)

            ax.scatter(points[start_idx:end_idx, 0], points[start_idx:end_idx, 1], points[start_idx:end_idx, 2],
                       c=colors[start_idx:end_idx], s=0.2)

            displayed_points = end_idx
            counter_text = f'Points displayed: {displayed_points}/{total_points} --- {((end_idx / total_points) * 100):.1f}%'
            counter_text_obj.set_text(counter_text)

            plt.draw()
            plt.gcf().canvas.manager.set_window_title('Neptun\'s Eye - 2D Visualization')
            plt.pause(kwargs['pause_interval'])

            plt.show()

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

