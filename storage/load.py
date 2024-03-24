import joblib
import laspy
import pandas as pd
import numpy as np
import onnx


def load_onnx(onnx_file_path):
    onnx_model = onnx.load(onnx_file_path)
    print("Model został pomyślnie wczytany z pliku ONNX:", onnx_file_path)
    return onnx_model

def read_las_file(file_path):
    las = laspy.read(file_path)
    columns = [dimension.name for dimension in las.point_format.dimensions]
    data = np.vstack([getattr(las, dimension) for dimension in columns]).transpose()
    df = pd.DataFrame(data, columns=columns)
    return df
