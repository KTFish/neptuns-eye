import numpy as np
import pandas as pd
import laspy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from tqdm.auto import tqdm
from preprocess import split_las_file


def read_las_file(file_path):
    las = laspy.read(file_path)
    columns = [dimension.name for dimension in las.point_format.dimensions]
    data = np.vstack([getattr(las, dimension) for dimension in columns]).transpose()
    df = pd.DataFrame(data, columns=columns)
    return df


def prepare_data(df, target_column):
    columns_to_delete = ['synthetic', 'key_point', 'withheld', 'user_data', 'point_source_id']
    df = df.drop(columns=columns_to_delete)

    # Sampling 1% of the data for quicker results
    df_sampled = df.sample(frac=1, random_state=42)

    X = df_sampled.drop(columns=[target_column])
    y = df_sampled[target_column]
    return train_test_split(X, y, test_size=0.2, random_state=42)


def random_forest_classification(X_train, X_test, y_train, y_test):
    n_estimators = 100
    clf = RandomForestClassifier(n_estimators=n_estimators, random_state=42)
    print(f"[INFO] Training random forest on: n_estimators: {n_estimators}")
    for _ in tqdm(range(1), desc="Training Progress"):
        clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
    return y_pred
    # return np.concatenate((y_pred, y_train), axis=0)
