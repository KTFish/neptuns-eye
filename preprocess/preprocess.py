from sklearn.model_selection import train_test_split


def prepare_data_training(df, target_column="classification", sample_rate=0.1, test_size=0.2, random_state=42):
    """
    Prepare data for training a machine learning model by performing the following steps:
    1. Drop specified columns from the DataFrame.
    2. Sample the DataFrame with a specified sampling rate.
    3. Split the sampled data into features (x) and target variable (y).
    4. Split the data into training and testing sets.

    Parameters:
    - df (DataFrame): The input DataFrame containing the dataset.
    - target_column (str): The name of the target column in the DataFrame. Default is "classification".
    - sample_rate (float): The fraction of samples to include in the sampled DataFrame.
    Should be between 0 and 1. Default is 0.1.
    - test_size (float): The proportion of the dataset to include in the test split.
    Should be between 0 and 1. Default is 0.2.
    - random_state (int): Controls the randomness of the sampling and splitting operations. Default is 42.

    Returns:
    - Tuple: A tuple containing four elements - X_train, X_test, y_train, y_test, where:
        - X_train (DataFrame): The features for training.
        - X_test (DataFrame): The features for testing.
        - y_train (Series): The target variable for training.
        - y_test (Series): The target variable for testing.
    """
    columns_to_delete = ['synthetic', 'key_point', 'withheld', 'user_data', 'point_source_id']
    df = df.drop(columns=columns_to_delete)

    df_sampled = df.sample(frac=sample_rate, random_state=random_state)

    x = df_sampled.drop(columns=[target_column])
    y = df_sampled[target_column]

    return train_test_split(x, y, test_size=test_size, random_state=random_state)


def prepare_data_prediction(df, target_column="classification", sample_rate=0.1, random_state=42):
    """
    Prepare data for making predictions using a trained machine learning model by performing the following steps:
    1. Drop specified columns from the DataFrame.
    2. Sample the DataFrame with a specified sampling rate.
    3. Separate the sampled data into features and target variable.

    Parameters:
    - df (DataFrame): The input DataFrame containing the dataset.
    - target_column (str): The name of the target column in the DataFrame. Default is "classification".
    - sample_rate (float): The fraction of samples to include in the sampled DataFrame.
    Should be between 0 and 1. Default is 0.1.
    - random_state (int): Controls the randomness of the sampling operation. Default is 42.

    Returns:
    - Tuple: A tuple containing two elements - test_features and test_labels, where:
        - test_features (DataFrame): The features of the data to be used for prediction.
        - test_labels (Series): The corresponding target variable values for the prediction dataset.
    """
    columns_to_delete = ['synthetic', 'key_point', 'withheld', 'user_data', 'point_source_id']
    df = df.drop(columns=columns_to_delete)
    df_sampled = df.sample(frac=sample_rate, random_state=random_state)

    test_features = df_sampled.drop(columns=[target_column])
    test_labels = df_sampled[target_column]

    return test_features, test_labels
