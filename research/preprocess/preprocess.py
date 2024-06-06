from sklearn.model_selection import train_test_split


def prepare_data_training(df, target_column="classification", test_size=0.2, random_state=42):
    """
    Split data into training and test sets by keeping specified columns and using specified target.

    Parameters:
    df (DataFrame): Input data frame.
    target_column (str): Column name to be used as the target variable. Default is "classification".
    test_size (float): Proportion of the dataset to include in the test split. Default is 0.2.
    random_state (int): Controls the shuffling applied to the data before applying the split. Default is 42.

    Returns:
    tuple: Training and test sets for features and target.
    """
    columns_to_keep = ['Z', 'red', 'green', 'blue', 'intensity',
                       'number_of_returns', 'return_number', 'edge_of_flight_line', 'scan_angle_rank', target_column]

    df = df[columns_to_keep]
    x = df.drop(columns=[target_column])
    y = df[target_column]

    return train_test_split(x, y, test_size=test_size, random_state=random_state)


def prepare_data_prediction(df, target_column="classification"):
    """
    Prepare prediction data by keeping specified columns and separating features from the target.

    Parameters:
    df (DataFrame): Input data frame.
    target_column (str): Column name to be used as the target variable. Default is "classification".

    Returns:
    tuple: Features and target labels for prediction.
    """
    columns_to_keep = ['Z', 'red', 'green', 'blue', 'intensity',
                       'number_of_returns', 'return_number', 'edge_of_flight_line', 'scan_angle_rank', target_column]

    df = df[columns_to_keep]
    test_features = df.drop(columns=[target_column])
    test_labels = df[target_column]

    return test_features, test_labels
