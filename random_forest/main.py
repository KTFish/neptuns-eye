import matplotlib.pyplot as plt
from train import *
from sample_points import sample_las_file
from visualize import visualize_predictions
from preprocess import preprocess_pipeline

import laspy
import pandas as pd


def read_las_file(file_path):
    las = laspy.read(file_path)
    columns = [dimension.name for dimension in las.point_format.dimensions]
    data = np.vstack([getattr(las, dimension) for dimension in columns]).transpose()
    df = pd.DataFrame(data, columns=columns)
    return df


def load_data_to_df(file_path):
    df = read_las_file(file_path)

    y = df['classification']
    X = df.drop(columns=['classification'])
    return X, y


if __name__ == '__main__':
    file_path = preprocess_pipeline(sample_rate=False)
    target_column = 'classification'

    # root = '../data/WMII_CLASS_LIGHT'
    root = '../data/WMII_CLASS'
    train_path = f"{root}_TRAIN.las"
    test_path = f"{root}_TEST.las"

    X_train, y_train = load_data_to_df(train_path)
    X_test, y_test = load_data_to_df(test_path)

    predictions = random_forest_classification(X_train, X_test, y_train, y_test)

    # Read the LAS file again to get the original x, y, z coordinates
    las = laspy.read(test_path)
    visualize_predictions(las, predictions)
