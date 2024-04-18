import joblib
import laspy
import pandas as pd
import numpy as np
import onnx


def load_joblib(joblib_file_path):
    model = joblib.load(joblib_file_path)
    if model:
        print("Model successfully loaded from the file.")
        return model
    else:
        print("Failed to load the model from the file.")
        return None


def load_onnx(onnx_file_path):
    onnx_model = None
    try:
        onnx_model = onnx.load(onnx_file_path)
        print("The model has been successfully loaded from the ONNX file:", onnx_file_path)
    except Exception as e:
        print("An error occurred while loading the ONNX model:", e)
    return onnx_model


def read_las_file(file_path):
    """
    Read data from a LAS (Log ASCII Standard) file and convert it into a pandas DataFrame.

    Parameters:
    - file_path (str): The path to the LAS file to be read.

    Returns:
    - DataFrame: A pandas DataFrame containing the data from the LAS file, with each row representing a point.
    The columns of the DataFrame correspond to different dimensions of the LAS file.
    """
    las = laspy.read(file_path)
    columns = [dimension.name for dimension in las.point_format.dimensions]
    data = np.vstack([getattr(las, dimension) for dimension in columns]).transpose()
    df = pd.DataFrame(data, columns=columns)
    return df
