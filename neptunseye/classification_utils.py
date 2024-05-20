import joblib


class ClassificationUtils:

    @staticmethod
    def prepare_data_prediction(df, target_column="classification", random_state=42):
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
        df_sampled = df

        test_features = df_sampled.drop(columns=[target_column])
        test_labels = df_sampled[target_column]

        return test_features, test_labels

    @staticmethod
    def load_joblib(joblib_file_path):
        model = joblib.load(joblib_file_path)
        if model:
            return model
        else:
            return None