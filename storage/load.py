import joblib
import laspy
import pandas as pd
import numpy as np


def load_model(filename):
    return joblib.load(filename)


def read_las_file(file_path):
    las = laspy.read(file_path)
    columns = [dimension.name for dimension in las.point_format.dimensions]
    data = np.vstack([getattr(las, dimension) for dimension in columns]).transpose()
    df = pd.DataFrame(data, columns=columns)
    return df
