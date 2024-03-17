import laspy
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


def read_las_file(file_path):
    las = laspy.read(file_path)
    columns = [dimension.name for dimension in las.point_format.dimensions]
    data = np.vstack([getattr(las, dimension) for dimension in columns]).transpose()
    df = pd.DataFrame(data, columns=columns)
    return df


def write_las_file(df, output_file_path, new_classification):
    # Tworzenie nowego DataFrame z nową wartością classification
    df['classification'] = new_classification

    # Tworzenie nowego obiektu pliku LAS
    las = laspy.create(point_format=2)

    # Przypisanie danych z DataFrame do odpowiednich pól w pliku LAS
    for column in df.columns:
        if column in las.point_format.dimension_names:
            setattr(las, column, df[column].values)

    # Zapisanie pliku LAS
    las.write(output_file_path)


def columns_names(las_file_path):
    las = laspy.read(las_file_path)
    column_names = [dimension.name for dimension in las.point_format.dimensions]
    print(column_names)


def prepare_data_training(df, target_column, sample_rate=0.1, test_size=0.2, random_state=42):
    columns_to_delete = ['synthetic', 'key_point', 'withheld', 'user_data', 'point_source_id']
    df = df.drop(columns=columns_to_delete)

    df_sampled = df.sample(frac=sample_rate, random_state=random_state)

    x = df_sampled.drop(columns=[target_column])
    y = df_sampled[target_column]
    return train_test_split(x, y, test_size=test_size, random_state=random_state)


def prepare_data_predict(df, target_column, sample_rate=0.1, random_state=42):
    columns_to_delete = ['synthetic', 'key_point', 'withheld', 'user_data', 'point_source_id']
    df = df.drop(columns=columns_to_delete)
    df_sampled = df.sample(frac=sample_rate, random_state=random_state)

    test_features = df_sampled.drop(columns=[target_column])  # Usuń tylko kolumny nielabelowe
    test_labels = df_sampled[target_column]  # Zachowaj tylko kolumnę z etykietami klasyfikacji

    return test_features, test_labels

