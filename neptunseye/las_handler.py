from typing import List, Any
import laspy
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import threading
from concurrent.futures import ThreadPoolExecutor
import plotly.graph_objects as go
import time
import CTkToolTip

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

    def visualize_las_2d_plotly(self, stride: int = 25):
        points = self.data_frame[['X', 'Y', 'Z']].values
        colors = self.data_frame[['red', 'green', 'blue']].values / 65535.0

        points = points[::stride]
        colors = colors[::stride]

        # Convert RGB colors to hexadecimal format
        hex_colors = ['#%02x%02x%02x' % tuple(int(255 * c) for c in color) for color in colors]

        fig = go.Figure()

        fig.add_trace(go.Scatter3d(
            x=points[:, 0],
            y=points[:, 1],
            z=points[:, 2],
            mode='markers',
            marker=dict(
                size=2,
                color=hex_colors  # Use hexadecimal colors
            )
        ))

        fig.update_layout(scene=dict(
            xaxis=dict(showticklabels=False),
            yaxis=dict(showticklabels=False),
            zaxis=dict(showticklabels=False)
        ))

        fig.show()

    def visualize_las_2d_matplotlib(self, stride: int = 15, batch: bool = False, **kwargs):
        """kwargs: batch_size, pause_interval"""

        if not batch:
            x = self.data_frame['X']
            y = self.data_frame['Y']
            z = self.data_frame['Z']

            r = self.data_frame['red'] / 65535.0
            g = self.data_frame['green'] / 65535.0
            b = self.data_frame['blue'] / 65535.0

            colors = np.column_stack((r, g, b))

            fig = plt.figure()
            fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(x, y, z, marker='.', c=colors, s=0.5)

            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.margins(0)
            ax.set_title('')

            plt.gcf().canvas.manager.set_window_title('Neptun\'s Eye - 2D Visualization')
            plt.show()

        else:
            points = self.data_frame[['X', 'Y', 'Z']].values
            colors = self.data_frame[['red', 'green', 'blue']].values / 65535.0

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
        print(df)
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

