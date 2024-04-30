from typing import List

import laspy
import numpy as np
import pandas as pd
import polyscope as ps
import plotly.graph_objects as go


class LasHandler(object):

    __file_path: str
    __file_loaded: bool
    __las: laspy.LasData
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

    def visualize_las_plotly(self, stride: int = 25, data_frame: pd.DataFrame = None):

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

    def visualize_las_polyscope(self, stride: int = 25, data_frame: pd.DataFrame = None) -> None:

        if data_frame is None:
            data_frame = self.data_frame
        else:
            data_frame = data_frame

        points = np.vstack((data_frame.X, data_frame.Y, data_frame.Z)).T
        colors = np.vstack((data_frame.red, data_frame.green, data_frame.blue)).T / 65025

        classifications = data_frame.classification.values
        class_color_map = {
            0: [1.0, 1.0, 1.0],  # 0 never classified - white
            1: [0.0, 0.0, 0.0],  # 1 unclassified - black
            11: [0.0, 0.0, 1.0],  # 11 ground - blue
            13: [0.0, 0.5, 0.0],  # 13 vegetation - green
            15: [0.0, 1.0, 1.0],  # 15 building - cyjan
            17: [0.5, 0.5, 0.5],  # 17 main road - gray
            19: [1.0, 0.0, 0.0],  # 19 power lines - red
            25: [0.6, 0.29, 0.0],  # 25 minor road - brown
        }
        classification = np.array([class_color_map[class_val] for class_val in classifications])

        ps.init()

        ps.set_up_dir("z_up")
        ps.set_front_dir("x_front")
        ps.set_navigation_style("turntable")

        cloud = ps.register_point_cloud("Point cloud", points[::stride], radius=0.0003, point_render_mode="quad")
        cloud.add_color_quantity("classification", classification[::stride], enabled=True)
        cloud.add_color_quantity("default", colors[::stride], enabled=True)

        ps.show()

    def __get_unique_classes(self) -> List[int]:
        return self.data_frame['classification'].unique().tolist()

    def create_dataframe(self):

        columns = [dimension.name for dimension in self.las.point_format.dimensions]
        data = np.vstack([getattr(self.las, dimension) for dimension in columns]).transpose()
        df = pd.DataFrame(data, columns=columns)
        return df

    def save_las_file(self, file_path: str = None) -> None:
        las = laspy.create(point_format=2)

        for column in self.data_frame.columns:
            if column in las.point_format.dimension_names:
                setattr(las, column, self.data_frame[column].values)

        if file_path is None:
            file_path = self.__file_path

        try:
            las.write(file_path)
        except Exception as e:
            self.__exception = e



    @property
    def file_path(self):
        return self.__file_path

    @file_path.setter
    def file_path(self, value):
        if not isinstance(value, str):
            raise ValueError("File path must be a string")
        self.__file_path = value

    @property
    def file_loaded(self):
        return self.__file_loaded

    @file_loaded.setter
    def file_loaded(self, value):
        if not isinstance(value, bool):
            raise ValueError("File loaded status must be a boolean")
        self.__file_loaded = value

    @property
    def las(self):
        return self.__las

    @las.setter
    def las(self, value):
        if not isinstance(value, laspy.LasData):
            raise ValueError("LAS data must be an instance of laspy.LasData")
        self.__las = value

    @property
    def exception(self):
        return self.__exception

    @exception.setter
    def exception(self, value):
        if not isinstance(value, Exception):
            raise ValueError("Exception must be an instance of Exception")
        self.__exception = value

    @property
    def data_frame(self):
        return self.__data_frame

    @data_frame.setter
    def data_frame(self, value):
        if not isinstance(value, pd.DataFrame) and value is not None:
            raise ValueError("Data frame must be a pandas DataFrame")
        self.__data_frame = value

    @property
    def unique_classes(self) -> List[int]:
        return self.__get_unique_classes()

    @unique_classes.setter
    def unique_classes(self, unique_classes: List[int]) -> None:
        self.__unique_classes = unique_classes
