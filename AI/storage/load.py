import joblib
import laspy
import pandas as pd
import numpy as np


def load_joblib(joblib_file_path):
    model = joblib.load(joblib_file_path)
    if model:
        print("Model successfully loaded from the file.")
        return model
    else:
        print("Failed to load the model from the file.")
        return None


def read_las_file(file_path):

    las = laspy.read(file_path)
    columns = [dimension.name for dimension in las.point_format.dimensions]
    data = np.vstack([getattr(las, dimension) for dimension in columns]).transpose()
    df = pd.DataFrame(data, columns=columns)
    return df
