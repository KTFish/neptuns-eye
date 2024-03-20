from sklearn.model_selection import train_test_split


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


def prepare_data_prediction(df, sample_rate=0.1, random_state=None, columns_to_delete=None):
    if columns_to_delete is None:
        columns_to_delete = ['synthetic', 'key_point', 'withheld', 'user_data', 'point_source_id']

    df_cleaned = df.drop(columns=columns_to_delete)

    df_sampled = df_cleaned.sample(frac=sample_rate, random_state=random_state)

    return df_sampled

