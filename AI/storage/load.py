import joblib
import laspy
import pandas as pd
import numpy as np

from utils.data_normalization import rgb_to_grayscale

def load_joblib(joblib_file_path):
    """
        Load a model from a joblib file and return it, printing a success or failure message.
    """
    model = joblib.load(joblib_file_path)
    if model:
        print("Model successfully loaded from the file.")
        return model
    else:
        print("Failed to load the model from the file.")
        return None


def read_las_file(file_path):
    """
        Read a LAS file using laspy, extract and return point data as a pandas DataFrame.
    """
    las = laspy.read(file_path)
    columns = [dimension.name for dimension in las.point_format.dimensions]
    data = np.vstack([getattr(las, dimension) for dimension in columns]).transpose()
    df = pd.DataFrame(data, columns=columns)
    return df


def read_las_file_filtered(file_path):
    """
    Read a LAS file using laspy, extract and return point data as a pandas DataFrame,
    excluding specified columns and converting RGB to grayscale.
    """
    exclude_columns = ['user_data', 'point_source_id', 'withheld', 'key_point', 'synthetic', 'scan_direction_flag']
    las = laspy.read(file_path)
    columns = [dimension.name for dimension in las.point_format.dimensions if dimension.name not in exclude_columns]
    data = np.vstack([getattr(las, dimension) for dimension in columns]).transpose()
    df = pd.DataFrame(data, columns=columns)

    if {'red', 'green', 'blue'}.issubset(df.columns):
        df = rgb_to_grayscale(df)

    return df
