from sklearn.model_selection import train_test_split


def prepare_data_training(df, target_column="classification", test_size=0.2, random_state=42):
    """
        Split data into training and test sets by removing specified columns and using specified target.
    """
    columns_to_delete = ['synthetic', 'key_point', 'withheld', 'user_data', 'point_source_id']
    df = df.drop(columns=columns_to_delete)

    x = df.drop(columns=[target_column])
    y = df[target_column]

    return train_test_split(x, y, test_size=test_size, random_state=random_state)


def prepare_data_prediction(df, target_column="classification"):
    """
        Prepare prediction data by removing specified columns and separating features from the target.
    """
    columns_to_delete = ['synthetic', 'key_point', 'withheld', 'user_data', 'point_source_id']
    df = df.drop(columns=columns_to_delete)

    test_features = df.drop(columns=[target_column])
    test_labels = df[target_column]

    return test_features, test_labels
